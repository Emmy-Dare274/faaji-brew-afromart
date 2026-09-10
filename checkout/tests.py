from decimal import Decimal
from unittest.mock import MagicMock, patch

from django.contrib.auth import get_user_model
from django.core import mail
from django.test import TestCase
from django.urls import reverse

from basket.models import Basket, BasketItem
from products.models import Category, Product
from .forms import OrderForm
from .models import Order, OrderLineItem
from .services import create_order_from_basket
from .webhook_handler import StripeWH_Handler

User = get_user_model()


class FakeStripeObject:

    """ A stand-in for the Stripe SDK object the real webhook passes
    in event["data"]["object"]. Only .to_dict() is needed, since
    that's the only method the handler actually calls on it. """

    def __init__(self, data):
        self._data = data

    def to_dict(self):
        return self._data


class OrderModelTests(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name="Traditional Wear")
        self.product = Product.objects.create(
            category=self.category, name="Agbada", description="x", price=Decimal("50.00"),
        )
        self.user = User.objects.create_user(username="buyer", password="testpass123")

    def _make_order(self):
        return Order.objects.create(
            user=self.user, full_name="Buyer Name", email="buyer@example.com",
            phone_number="1234567890", address_line1="1 Test Street",
            town_or_city="Testville", postcode="12345", country="IE",
        )

    def test_order_number_is_generated_automatically(self):
        order = self._make_order()
        self.assertTrue(order.order_number)
        self.assertEqual(len(order.order_number), 32)

    def test_two_orders_never_share_an_order_number(self):
        first = self._make_order()
        second = self._make_order()
        self.assertNotEqual(first.order_number, second.order_number)

    def test_update_totals_adds_standard_delivery_below_the_free_threshold(self):
        order = self._make_order()
        OrderLineItem.objects.create(
            order=order, product=self.product, quantity=1, price_at_purchase=Decimal("50.00"),
        )
        order.update_totals()
        self.assertEqual(order.order_total, Decimal("50.00"))
        self.assertEqual(order.delivery_cost, Decimal("4.99"))
        self.assertEqual(order.grand_total, Decimal("54.99"))

    def test_update_totals_gives_free_delivery_at_the_threshold(self):
        order = self._make_order()
        OrderLineItem.objects.create(
            order=order, product=self.product, quantity=2, price_at_purchase=Decimal("50.00"),
        )
        order.update_totals()
        self.assertEqual(order.order_total, Decimal("100.00"))
        self.assertEqual(order.delivery_cost, Decimal("0.00"))
        self.assertEqual(order.grand_total, Decimal("100.00"))

    def test_lineitem_total_multiplies_price_by_quantity(self):
        order = self._make_order()
        item = OrderLineItem.objects.create(
            order=order, product=self.product, quantity=3, price_at_purchase=Decimal("50.00"),
        )
        self.assertEqual(item.lineitem_total, Decimal("150.00"))


class OrderFormTests(TestCase):

    def test_valid_data_is_accepted(self):
        form = OrderForm(data={
            "full_name": "Jane Shopper", "email": "jane@example.com", "phone_number": "1234567890",
            "address_line1": "1 Test Street", "address_line2": "", "town_or_city": "Testville",
            "postcode": "12345", "country": "IE",
        })
        self.assertTrue(form.is_valid())

    def test_missing_address_is_rejected(self):
        form = OrderForm(data={
            "full_name": "Jane Shopper", "email": "jane@example.com", "phone_number": "1234567890",
            "address_line1": "", "town_or_city": "Testville", "postcode": "12345", "country": "IE",
        })
        self.assertFalse(form.is_valid())


class CreateOrderFromBasketTests(TestCase):

    """ Covers the service that turns a basket into a real order,
    including the rule that price_at_purchase is locked in at
    checkout time rather than always reading the live product
    price. """

    def setUp(self):
        self.category = Category.objects.create(name="Ankara Fabrics")
        self.product = Product.objects.create(
            category=self.category, name="Adire Print", description="x", price=Decimal("30.00"),
        )
        self.user = User.objects.create_user(username="buyer", password="testpass123")
        self.basket = Basket.objects.create(user=self.user)
        BasketItem.objects.create(basket=self.basket, product=self.product, quantity=1)

    def _address_data(self):
        return {
            "full_name": "Buyer Name", "email": "buyer@example.com", "phone_number": "123",
            "address_line1": "1 Test St", "address_line2": "", "town_or_city": "Testville",
            "postcode": "12345", "country": "IE",
        }

    def test_creates_an_order_with_matching_line_items(self):
        order = create_order_from_basket(self.user, self.basket, self._address_data())
        self.assertEqual(order.lineitems.count(), 1)
        self.assertEqual(order.grand_total, Decimal("34.99"))  # 30.00 + 4.99 delivery

    def test_price_at_purchase_is_locked_in_even_if_the_product_price_changes_later(self):
        order = create_order_from_basket(self.user, self.basket, self._address_data())
        self.product.price = Decimal("99.00")
        self.product.save()
        line_item = order.lineitems.first()
        self.assertEqual(line_item.price_at_purchase, Decimal("30.00"))


class CheckoutViewTests(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name="Beads & Jewellery")
        self.product = Product.objects.create(
            category=self.category, name="Anklet", description="x", price=Decimal("12.00"),
            stock_quantity=10,
        )
        self.user = User.objects.create_user(username="buyer", password="testpass123")

    def test_logged_out_user_is_redirected_to_login(self):
        response = self.client.get(reverse("checkout:checkout"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("account_login"), response.url)

    def test_logged_in_user_with_an_empty_basket_is_redirected_with_an_error(self):
        self.client.login(username="buyer", password="testpass123")
        response = self.client.get(reverse("checkout:checkout"), follow=True)
        self.assertRedirects(response, reverse("products:product_list"))

    def test_logged_in_user_with_items_sees_the_checkout_form(self):
        self.client.login(username="buyer", password="testpass123")
        self.client.post(
            reverse("basket:add_to_basket", args=[self.product.slug]), {"quantity": 1}
        )
        response = self.client.get(reverse("checkout:checkout"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Anklet")

    @patch("checkout.views.stripe.PaymentIntent.create")
    def test_valid_submission_creates_an_order_and_shows_the_payment_page(self, mock_create):
        mock_create.return_value = MagicMock(id="pi_test123", client_secret="secret_test123")
        self.client.login(username="buyer", password="testpass123")
        self.client.post(
            reverse("basket:add_to_basket", args=[self.product.slug]), {"quantity": 1}
        )
        response = self.client.post(reverse("checkout:checkout"), {
            "full_name": "Jane Shopper", "email": "jane@example.com", "phone_number": "1234567890",
            "address_line1": "1 Test Street", "address_line2": "", "town_or_city": "Testville",
            "postcode": "12345", "country": "IE",
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Order.objects.filter(email="jane@example.com").exists())
        self.assertTemplateUsed(response, "checkout/checkout_payment.html")


class CheckoutSuccessViewTests(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name="Homeware")
        self.owner = User.objects.create_user(username="owner", password="testpass123")
        self.other_user = User.objects.create_user(username="intruder", password="testpass123")
        self.order = Order.objects.create(
            user=self.owner, full_name="Owner", email="owner@example.com", phone_number="123",
            address_line1="1 Test St", town_or_city="Testville", postcode="12345", country="IE",
        )

    def test_owner_can_view_their_own_success_page(self):
        self.client.login(username="owner", password="testpass123")
        response = self.client.get(
            reverse("checkout:checkout_success", args=[self.order.order_number])
        )
        self.assertEqual(response.status_code, 200)

    def test_another_user_cannot_view_someone_elses_order(self):
        self.client.login(username="intruder", password="testpass123")
        response = self.client.get(
            reverse("checkout:checkout_success", args=[self.order.order_number])
        )
        self.assertEqual(response.status_code, 404)


class WebhookHandlerTests(TestCase):

    """ Covers the actual business logic Stripe's webhook triggers:
    moving a paid order out of pending and sending the confirmation
    email, including the idempotency guard that stops a customer
    getting two confirmation emails if Stripe redelivers the same
    event, which it is explicitly allowed to do."""

    def setUp(self):
        self.category = Category.objects.create(name="Ankara Fabrics")
        self.product = Product.objects.create(
            category=self.category, name="Adire Print", description="x", price=Decimal("30.00"),
        )
        self.user = User.objects.create_user(username="buyer", password="testpass123")
        self.order = Order.objects.create(
            user=self.user, full_name="Buyer Name", email="buyer@example.com", phone_number="123",
            address_line1="1 Test St", town_or_city="Testville", postcode="12345", country="IE",
        )
        OrderLineItem.objects.create(
            order=self.order, product=self.product, quantity=1, price_at_purchase=Decimal("30.00"),
        )
        self.order.update_totals()

    def _succeeded_event(self):
        return {
            "type": "payment_intent.succeeded",
            "data": {
                "object": FakeStripeObject({"metadata": {"order_number": self.order.order_number}})
            },
        }

    def test_confirmed_payment_moves_the_order_to_processing_and_sends_an_email(self):
        handler = StripeWH_Handler(request=None)
        handler.handle_payment_intent_succeeded(self._succeeded_event())

        self.order.refresh_from_db()
        self.assertEqual(self.order.status, Order.Status.PROCESSING)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn(self.order.order_number, mail.outbox[0].subject)

    def test_the_same_event_delivered_twice_only_sends_one_email(self):

        """ Stripe explicitly documents that a webhook event can
        arrive more than once for the same payment, so the handler
        has to treat the second delivery as a no-op rather than
        confirming the order (and emailing the customer) again. """

        handler = StripeWH_Handler(request=None)
        handler.handle_payment_intent_succeeded(self._succeeded_event())
        handler.handle_payment_intent_succeeded(self._succeeded_event())

        self.order.refresh_from_db()
        self.assertEqual(self.order.status, Order.Status.PROCESSING)
        self.assertEqual(len(mail.outbox), 1)

    def test_an_unknown_order_number_is_handled_without_raising_an_error(self):
        event = {
            "type": "payment_intent.succeeded",
            "data": {"object": FakeStripeObject({"metadata": {"order_number": "DOES-NOT-EXIST"}})},
        }
        handler = StripeWH_Handler(request=None)
        response = handler.handle_payment_intent_succeeded(event)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(mail.outbox), 0)
