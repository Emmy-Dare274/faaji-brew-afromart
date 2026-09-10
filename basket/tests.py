from decimal import Decimal

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory, TestCase
from django.urls import reverse

from products.models import Category, Product, ProductVariant
from .models import Basket, BasketItem
from .services import add_item, get_or_create_basket, merge_guest_basket_into_user

User = get_user_model()


class BasketModelTests(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name="Spices & Sauce Kits")
        self.product = Product.objects.create(
            category=self.category, name="Pepper Soup Kit", description="x",
            price=Decimal("10.00"), stock_quantity=20,
        )
        self.basket = Basket.objects.create()

    def test_empty_basket_totals_are_zero(self):
        self.assertEqual(self.basket.total, 0)
        self.assertEqual(self.basket.item_count, 0)
        self.assertFalse(self.basket.qualifies_for_free_delivery)

    def test_basket_item_line_total_without_variant(self):
        item = BasketItem.objects.create(basket=self.basket, product=self.product, quantity=3)
        self.assertEqual(item.unit_price, Decimal("10.00"))
        self.assertEqual(item.line_total, Decimal("30.00"))

    def test_basket_item_line_total_includes_variant_price_adjustment(self):
        variant = ProductVariant.objects.create(
            product=self.product, variant_type="size", value="Large",
            price_adjustment=Decimal("2.50"),
        )
        item = BasketItem.objects.create(
            basket=self.basket, product=self.product, variant=variant, quantity=2,
        )
        self.assertEqual(item.unit_price, Decimal("12.50"))
        self.assertEqual(item.line_total, Decimal("25.00"))

    def test_basket_qualifies_for_free_delivery_at_the_threshold(self):
        # 6 x 10.00 = 60.00
        BasketItem.objects.create(basket=self.basket, product=self.product, quantity=6)
        self.assertTrue(self.basket.qualifies_for_free_delivery)
        self.assertEqual(self.basket.amount_to_free_delivery, Decimal("0.00"))

    def test_amount_to_free_delivery_when_under_the_threshold(self):
        BasketItem.objects.create(basket=self.basket, product=self.product, quantity=1)  # 10.00
        self.assertEqual(self.basket.amount_to_free_delivery, Decimal("50.00"))


class BasketServiceTests(TestCase):

    """ Tests the service layer directly, using a bare RequestFactory
    request with a real session attached by hand (no middleware runs
    on a RequestFactory request otherwise), since get_or_create_basket
    and merge_guest_basket_into_user both need request.session. """

    def setUp(self):
        self.category = Category.objects.create(name="Homeware")
        self.product = Product.objects.create(
            category=self.category, name="Cushion", description="x",
            price=Decimal("15.00"), stock_quantity=10,
        )
        self.factory = RequestFactory()

    def _request_with_session(self, user=None):
        from django.contrib.sessions.backends.db import SessionStore
        request = self.factory.get("/")
        request.session = SessionStore()
        request.session.create()
        request.user = user or AnonymousUser()
        return request

    def test_get_or_create_basket_returns_the_same_basket_on_repeat_calls_for_a_guest(self):
        request = self._request_with_session()
        first = get_or_create_basket(request)
        second = get_or_create_basket(request)
        self.assertEqual(first.id, second.id)

    def test_get_or_create_basket_uses_the_user_not_the_session_when_logged_in(self):
        user = User.objects.create_user(username="shopper", password="testpass123")
        request = self._request_with_session(user=user)
        basket = get_or_create_basket(request)
        self.assertEqual(basket.user, user)

    def test_add_item_creates_a_new_basket_item(self):
        basket = Basket.objects.create()
        add_item(basket, self.product, quantity=2)
        self.assertEqual(basket.items.count(), 1)
        self.assertEqual(basket.items.first().quantity, 2)

    def test_add_item_increments_quantity_for_an_existing_line(self):
        basket = Basket.objects.create()
        add_item(basket, self.product, quantity=2)
        add_item(basket, self.product, quantity=3)
        self.assertEqual(basket.items.count(), 1)
        self.assertEqual(basket.items.first().quantity, 5)

    def test_merge_guest_basket_into_user_moves_items_and_removes_the_guest_basket(self):
        request = self._request_with_session()
        guest_basket = get_or_create_basket(request)
        add_item(guest_basket, self.product, quantity=2)

        user = User.objects.create_user(username="shopper", password="testpass123")
        merge_guest_basket_into_user(request, user)

        user_basket = Basket.objects.get(user=user)
        self.assertEqual(user_basket.items.first().quantity, 2)
        self.assertFalse(
            Basket.objects.filter(session_key=request.session.session_key, user=None).exists()
        )


class BasketViewTests(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name="Accessories")
        self.product = Product.objects.create(
            category=self.category, name="Tote Bag", description="x",
            price=Decimal("18.00"), stock_quantity=5,
        )

    def test_basket_detail_loads_for_a_guest(self):
        response = self.client.get(reverse("basket:basket_detail"))
        self.assertEqual(response.status_code, 200)

    def test_add_to_basket_creates_an_item_and_redirects(self):
        response = self.client.post(
            reverse("basket:add_to_basket", args=[self.product.slug]), {"quantity": 1}
        )
        self.assertRedirects(response, reverse("basket:basket_detail"))
        self.assertEqual(BasketItem.objects.count(), 1)

    def test_add_to_basket_rejects_a_quantity_above_available_stock(self):
        self.client.post(
            reverse("basket:add_to_basket", args=[self.product.slug]), {"quantity": 999}
        )
        self.assertEqual(BasketItem.objects.count(), 0)

    def test_update_basket_item_changes_the_quantity(self):
        self.client.post(
            reverse("basket:add_to_basket", args=[self.product.slug]), {"quantity": 1}
        )
        item = BasketItem.objects.first()
        self.client.post(
            reverse("basket:update_basket_item", args=[item.id]), {"quantity": 4}
        )
        item.refresh_from_db()
        self.assertEqual(item.quantity, 4)

    def test_setting_quantity_to_zero_removes_the_item(self):
        self.client.post(
            reverse("basket:add_to_basket", args=[self.product.slug]), {"quantity": 1}
        )
        item = BasketItem.objects.first()
        self.client.post(
            reverse("basket:update_basket_item", args=[item.id]), {"quantity": 0}
        )
        self.assertEqual(BasketItem.objects.count(), 0)

    def test_remove_basket_item_deletes_it(self):
        self.client.post(
            reverse("basket:add_to_basket", args=[self.product.slug]), {"quantity": 1}
        )
        item = BasketItem.objects.first()
        self.client.post(reverse("basket:remove_basket_item", args=[item.id]))
        self.assertEqual(BasketItem.objects.count(), 0)

    def test_a_different_session_cannot_modify_someone_elses_basket_item(self):
        self.client.post(
            reverse("basket:add_to_basket", args=[self.product.slug]), {"quantity": 1}
        )
        item = BasketItem.objects.first()
        self.client.cookies.clear()  # simulates a brand new, unrelated visitor
        response = self.client.post(
            reverse("basket:update_basket_item", args=[item.id]), {"quantity": 9}
        )
        self.assertEqual(response.status_code, 404)
