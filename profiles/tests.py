from decimal import Decimal

from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction
from django.test import TestCase
from django.urls import reverse

from basket.models import BasketItem
from checkout.models import Order, OrderLineItem
from products.models import Category, Product
from .forms import ProfileForm
from .models import UserProfile, WishList, WishListItem

User = get_user_model()


class UserProfileModelTests(TestCase):

    def test_string_representation_includes_the_username(self):
        user = User.objects.create_user(username="shopper", password="testpass123")
        profile = UserProfile.objects.create(user=user)
        self.assertEqual(str(profile), "Profile for shopper")


class WishListModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="shopper", password="testpass123")
        self.category = Category.objects.create(name="Accessories")
        self.product = Product.objects.create(
            category=self.category, name="Tote Bag", description="x", price=Decimal("18.00"),
        )

    def test_a_product_can_only_appear_once_on_the_same_wishlist(self):
        wishlist = WishList.objects.create(user=self.user)
        WishListItem.objects.create(wishlist=wishlist, product=self.product)
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                WishListItem.objects.create(wishlist=wishlist, product=self.product)


class ProfileFormTests(TestCase):

    def test_every_field_is_optional(self):
        # A brand new customer has no saved address yet, and My
        # Account still has to render without errors before they've
        # ever filled anything in.
        form = ProfileForm(data={})
        self.assertTrue(form.is_valid())

    def test_valid_full_data_is_accepted(self):
        form = ProfileForm(data={
            "default_full_name": "Jane Shopper", "default_phone_number": "1234567890",
            "default_address_line1": "1 Test Street", "default_address_line2": "",
            "default_town_or_city": "Testville", "default_postcode": "12345",
            "default_country": "IE",
        })
        self.assertTrue(form.is_valid())


class WishlistViewTests(TestCase):

    """ Covers issue #24 (shop directly from a wishlist) and the
    login-gating rule from issue #9. """

    def setUp(self):
        self.category = Category.objects.create(name="Homeware")
        self.product = Product.objects.create(
            category=self.category, name="Cushion", description="x", price=Decimal("15.00"),
        )
        self.user = User.objects.create_user(username="shopper", password="testpass123")

    def test_wishlist_page_requires_login(self):
        response = self.client.get(reverse("profiles:wishlist_detail"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("account_login"), response.url)

    def test_toggling_adds_then_removes_a_product(self):
        self.client.login(username="shopper", password="testpass123")
        url = reverse("profiles:toggle_wishlist", args=[self.product.slug])

        self.client.post(url)
        self.assertEqual(WishListItem.objects.count(), 1)

        self.client.post(url)
        self.assertEqual(WishListItem.objects.count(), 0)

    def test_ajax_toggle_returns_json_with_the_new_state(self):
        self.client.login(username="shopper", password="testpass123")
        response = self.client.post(
            reverse("profiles:toggle_wishlist", args=[self.product.slug]),
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["wishlisted"])

    def test_anonymous_ajax_toggle_gets_a_401_with_a_login_url(self):
        # Covers a real bug this project hit early on: silently
        # failing for a logged-out visitor instead of telling the
        # front end to prompt for login.
        response = self.client.post(
            reverse("profiles:toggle_wishlist", args=[self.product.slug]),
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertEqual(response.status_code, 401)
        self.assertIn("login_url", response.json())

    def test_wishlist_page_only_shows_the_logged_in_users_own_items(self):
        other_user = User.objects.create_user(username="other", password="testpass123")
        other_wishlist = WishList.objects.create(user=other_user)
        WishListItem.objects.create(wishlist=other_wishlist, product=self.product)

        self.client.login(username="shopper", password="testpass123")
        response = self.client.get(reverse("profiles:wishlist_detail"))
        self.assertNotContains(response, "Cushion")


class MyAccountViewTests(TestCase):

    """ Covers issue #10: managing saved delivery addresses. """

    def setUp(self):
        self.user = User.objects.create_user(username="shopper", password="testpass123")

    def test_page_requires_login(self):
        response = self.client.get(reverse("profiles:my_account"))
        self.assertEqual(response.status_code, 302)

    def test_visiting_creates_a_profile_automatically(self):
        self.client.login(username="shopper", password="testpass123")
        self.assertFalse(UserProfile.objects.filter(user=self.user).exists())
        self.client.get(reverse("profiles:my_account"))
        self.assertTrue(UserProfile.objects.filter(user=self.user).exists())

    def test_submitting_the_form_saves_the_new_details(self):
        self.client.login(username="shopper", password="testpass123")
        self.client.post(reverse("profiles:my_account"), {
            "default_full_name": "Jane Shopper", "default_phone_number": "1234567890",
            "default_address_line1": "1 Test Street", "default_address_line2": "",
            "default_town_or_city": "Testville", "default_postcode": "12345",
            "default_country": "IE",
        })
        profile = UserProfile.objects.get(user=self.user)
        self.assertEqual(profile.default_full_name, "Jane Shopper")


class OrderHistoryViewTests(TestCase):

    """ Covers issue #22: viewing order history and status. """

    def setUp(self):
        self.user = User.objects.create_user(username="shopper", password="testpass123")
        self.other_user = User.objects.create_user(username="other", password="testpass123")

    def test_page_requires_login(self):
        response = self.client.get(reverse("profiles:order_history"))
        self.assertEqual(response.status_code, 302)

    def test_only_shows_the_logged_in_users_own_orders(self):
        Order.objects.create(
            user=self.user, full_name="Me", email="me@example.com", phone_number="123",
            address_line1="1 Test St", town_or_city="Testville", postcode="12345", country="IE",
        )
        Order.objects.create(
            user=self.other_user, full_name="Other", email="other@example.com", phone_number="123",
            address_line1="2 Test St", town_or_city="Testville", postcode="12345", country="IE",
        )
        self.client.login(username="shopper", password="testpass123")
        response = self.client.get(reverse("profiles:order_history"))
        self.assertEqual(len(response.context["orders"]), 1)


class ReorderViewTests(TestCase):

    """ Covers the reorder feature built alongside order history:
    adding every item from a past order back into the basket in one
    go, skipping anything no longer available rather than failing
    the whole action. """

    def setUp(self):
        self.category = Category.objects.create(name="Spices & Sauce Kits")
        self.available_product = Product.objects.create(
            category=self.category, name="Jollof Kit", description="x",
            price=Decimal("10.00"), stock_quantity=10, is_active=True,
        )
        self.discontinued_product = Product.objects.create(
            category=self.category, name="Old Kit", description="x",
            price=Decimal("8.00"), stock_quantity=5, is_active=False,
        )
        self.out_of_stock_product = Product.objects.create(
            category=self.category, name="Sold Out Kit", description="x",
            price=Decimal("9.00"), stock_quantity=0, is_active=True,
        )
        self.user = User.objects.create_user(username="shopper", password="testpass123")
        self.order = Order.objects.create(
            user=self.user, full_name="Shopper", email="shopper@example.com", phone_number="123",
            address_line1="1 Test St", town_or_city="Testville", postcode="12345",
            country="IE",
        )
        available = [self.available_product, self.discontinued_product, self.out_of_stock_product]
        for product in available:
            OrderLineItem.objects.create(
                order=self.order, product=product, quantity=1, price_at_purchase=product.price,
            )

    def test_only_available_items_are_added_back_to_the_basket(self):
        self.client.login(username="shopper", password="testpass123")
        self.client.post(reverse("profiles:reorder", args=[self.order.order_number]))
        self.assertEqual(BasketItem.objects.count(), 1)
        self.assertEqual(BasketItem.objects.first().product, self.available_product)

    def test_cannot_reorder_someone_elses_order(self):
        User.objects.create_user(username="other", password="testpass123")
        self.client.login(username="other", password="testpass123")
        response = self.client.post(reverse("profiles:reorder", args=[self.order.order_number]))
        self.assertEqual(response.status_code, 404)
