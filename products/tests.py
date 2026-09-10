from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from checkout.models import Order, OrderLineItem
from .forms import CategoryForm, ProductForm, ReviewForm
from .models import Category, Product, ProductImage, Review

User = get_user_model()

# A minimal, valid 1x1 pixel GIF, used to give ImageField something
# real to validate without needing an actual image file on disk.
TINY_GIF = (
    b'GIF87a\x01\x00\x01\x00\x80\x01\x00\x00\x00\x00ccc,\x00\x00'
    b'\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;'
)


class CategoryModelTests(TestCase):

    def test_slug_is_generated_automatically_from_name(self):
        category = Category.objects.create(name="Ankara Fabrics")
        self.assertEqual(category.slug, "ankara-fabrics")

    def test_string_representation_is_the_name(self):
        category = Category.objects.create(name="Homeware")
        self.assertEqual(str(category), "Homeware")


class ProductModelTests(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name="Spices & Sauce Kits")

    def test_slug_and_sku_are_generated_automatically(self):
        product = Product.objects.create(
            category=self.category, name="Jollof Spice Kit",
            description="Everything you need.", price=Decimal("12.99"),
        )
        self.assertEqual(product.slug, "jollof-spice-kit")
        self.assertTrue(product.sku)
        self.assertTrue(product.sku.startswith("SPI"))

    def test_two_products_never_get_the_same_sku(self):
        first = Product.objects.create(
            category=self.category, name="Kit One", description="x", price=Decimal("5.00"),
        )
        second = Product.objects.create(
            category=self.category, name="Kit Two", description="x", price=Decimal("5.00"),
        )
        self.assertNotEqual(first.sku, second.sku)

    def test_in_stock_reflects_stock_quantity(self):
        in_stock = Product.objects.create(
            category=self.category, name="In Stock Item", description="x",
            price=Decimal("5.00"), stock_quantity=3,
        )
        out_of_stock = Product.objects.create(
            category=self.category, name="Out of Stock Item", description="x",
            price=Decimal("5.00"), stock_quantity=0,
        )
        self.assertTrue(in_stock.in_stock)
        self.assertFalse(out_of_stock.in_stock)

    def test_primary_image_prefers_the_image_marked_primary(self):
        product = Product.objects.create(
            category=self.category, name="Multi Image Product", description="x", price=Decimal("5.00"),
        )
        ProductImage.objects.create(product=product, image="products/first.jpg")
        second = ProductImage.objects.create(product=product, image="products/second.jpg", is_primary=True)
        self.assertEqual(product.primary_image, second)

    def test_primary_image_falls_back_to_first_uploaded_when_none_marked_primary(self):
        product = Product.objects.create(
            category=self.category, name="No Primary Marked", description="x", price=Decimal("5.00"),
        )
        first = ProductImage.objects.create(product=product, image="products/first.jpg")
        ProductImage.objects.create(product=product, image="products/second.jpg")
        self.assertEqual(product.primary_image, first)

    def test_primary_image_is_none_when_product_has_no_images(self):
        product = Product.objects.create(
            category=self.category, name="No Images", description="x", price=Decimal("5.00"),
        )
        self.assertIsNone(product.primary_image)


class ProductQuerySetTests(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name="Beads & Jewellery")

    def test_search_matches_name_and_description(self):
        Product.objects.create(
            category=self.category, name="Beaded Anklet", description="Handmade.", price=Decimal("10.00"),
        )
        Product.objects.create(
            category=self.category, name="Woven Bracelet", description="Features colourful beads.",
            price=Decimal("8.00"),
        )
        Product.objects.create(
            category=self.category, name="Plain Ring", description="Simple silver band.", price=Decimal("15.00"),
        )
        results = Product.objects.search("bead")
        self.assertEqual(results.count(), 2)

    def test_price_range_filters_correctly(self):
        cheap = Product.objects.create(
            category=self.category, name="Cheap Item", description="x", price=Decimal("5.00"),
        )
        pricey = Product.objects.create(
            category=self.category, name="Pricey Item", description="x", price=Decimal("50.00"),
        )
        results = Product.objects.price_range(min_price="10", max_price="100")
        self.assertIn(pricey, results)
        self.assertNotIn(cheap, results)

    def test_featured_only_returns_active_featured_products(self):
        Product.objects.create(
            category=self.category, name="Featured Active", description="x",
            price=Decimal("5.00"), is_featured=True, is_active=True,
        )
        Product.objects.create(
            category=self.category, name="Featured Inactive", description="x",
            price=Decimal("5.00"), is_featured=True, is_active=False,
        )
        self.assertEqual(Product.objects.featured().count(), 1)


class ReviewFormTests(TestCase):

    def test_valid_data_is_accepted(self):
        form = ReviewForm(data={"rating": 5, "title": "Loved it", "body": "Excellent quality."})
        self.assertTrue(form.is_valid())

    def test_rating_outside_the_five_star_scale_is_rejected(self):
        form = ReviewForm(data={"rating": 9, "title": "Loved it", "body": "Excellent quality."})
        self.assertFalse(form.is_valid())

    def test_missing_title_is_rejected(self):
        form = ReviewForm(data={"rating": 5, "title": "", "body": "Excellent quality."})
        self.assertFalse(form.is_valid())


class ProductFormTests(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name="Traditional Wear")

    def test_valid_data_is_accepted(self):
        form = ProductForm(data={
            "category": self.category.id, "name": "Agbada Set", "description": "Elegant.",
            "price": "45.00", "stock_quantity": 10, "is_featured": False, "is_active": True,
        })
        self.assertTrue(form.is_valid())

    def test_missing_price_is_rejected(self):
        form = ProductForm(data={
            "category": self.category.id, "name": "Agbada Set", "description": "Elegant.",
            "stock_quantity": 10,
        })
        self.assertFalse(form.is_valid())


class CategoryFormTests(TestCase):

    def test_valid_data_is_accepted(self):
        form = CategoryForm(data={
            "name": "New Category", "description": "", "is_active": True, "show_in_main_nav": True,
        })
        self.assertTrue(form.is_valid())

    def test_duplicate_name_is_rejected(self):
        Category.objects.create(name="Existing Category")
        form = CategoryForm(data={"name": "Existing Category", "is_active": True, "show_in_main_nav": True})
        self.assertFalse(form.is_valid())


class ProductListViewTests(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name="Ankara Fabrics")
        self.product = Product.objects.create(
            category=self.category, name="Sunburst Print", description="Bold pattern.",
            price=Decimal("20.00"), is_active=True,
        )
        self.inactive_product = Product.objects.create(
            category=self.category, name="Discontinued Print", description="x",
            price=Decimal("20.00"), is_active=False,
        )

    def test_product_list_only_shows_active_products(self):
        response = self.client.get(reverse("products:product_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sunburst Print")
        self.assertNotContains(response, "Discontinued Print")

    def test_filtering_by_category_slug(self):
        other_category = Category.objects.create(name="Homeware")
        Product.objects.create(
            category=other_category, name="Cushion Cover", description="x",
            price=Decimal("10.00"), is_active=True,
        )
        response = self.client.get(
            reverse("products:product_list_by_category", args=[self.category.slug])
        )
        self.assertContains(response, "Sunburst Print")
        self.assertNotContains(response, "Cushion Cover")

    def test_search_query_filters_results(self):
        response = self.client.get(reverse("products:product_list"), {"q": "Sunburst"})
        self.assertContains(response, "Sunburst Print")


class ProductDetailViewTests(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name="Accessories")
        self.product = Product.objects.create(
            category=self.category, name="Structured Handbag", description="x",
            price=Decimal("35.00"), is_active=True,
        )

    def test_active_product_detail_loads(self):
        response = self.client.get(
            reverse("products:product_detail", args=[self.product.slug])
        )
        self.assertEqual(response.status_code, 200)

    def test_unknown_slug_returns_404(self):
        response = self.client.get(
            reverse("products:product_detail", args=["does-not-exist"])
        )
        self.assertEqual(response.status_code, 404)


class ReviewWorkflowTests(TestCase):

    """ Covers issues #25, #26, and #27: writing, editing, and
    moderating reviews, including the purchase-required rule. """

    def setUp(self):
        self.category = Category.objects.create(name="Homeware")
        self.product = Product.objects.create(
            category=self.category, name="Cushion Set", description="x", price=Decimal("15.00"),
        )
        self.buyer = User.objects.create_user(username="buyer", password="testpass123")
        self.non_buyer = User.objects.create_user(username="nonbuyer", password="testpass123")

        order = Order.objects.create(
            user=self.buyer, full_name="Buyer", email="buyer@example.com",
            phone_number="1234567890", address_line1="1 Test St",
            town_or_city="Testville", postcode="12345", country="IE",
        )
        OrderLineItem.objects.create(
            order=order, product=self.product, quantity=1, price_at_purchase=Decimal("15.00"),
        )

    def test_logged_out_user_cannot_submit_a_review(self):
        self.client.post(
            reverse("products:add_review", args=[self.product.slug]),
            {"rating": 5, "title": "Great", "body": "Loved it."},
        )
        self.assertEqual(Review.objects.count(), 0)

    def test_non_purchaser_cannot_submit_a_review(self):
        self.client.login(username="nonbuyer", password="testpass123")
        self.client.post(
            reverse("products:add_review", args=[self.product.slug]),
            {"rating": 5, "title": "Great", "body": "Loved it."},
        )
        self.assertEqual(Review.objects.count(), 0)

    def test_purchaser_can_submit_one_review(self):
        self.client.login(username="buyer", password="testpass123")
        self.client.post(
            reverse("products:add_review", args=[self.product.slug]),
            {"rating": 5, "title": "Great", "body": "Loved it."},
        )
        self.assertEqual(Review.objects.count(), 1)
        self.assertFalse(Review.objects.first().is_approved)

    def test_purchaser_cannot_submit_a_second_review_for_the_same_product(self):
        self.client.login(username="buyer", password="testpass123")
        Review.objects.create(product=self.product, user=self.buyer, rating=4, title="First", body="Ok.")
        self.client.post(
            reverse("products:add_review", args=[self.product.slug]),
            {"rating": 5, "title": "Second", "body": "Better."},
        )
        self.assertEqual(Review.objects.count(), 1)

    def test_editing_a_review_resets_it_to_unapproved(self):
        self.client.login(username="buyer", password="testpass123")
        review = Review.objects.create(
            product=self.product, user=self.buyer, rating=4, title="Original", body="Ok.", is_approved=True,
        )
        self.client.post(
            reverse("products:edit_review", args=[review.id]),
            {"rating": 5, "title": "Updated", "body": "Even better now."},
        )
        review.refresh_from_db()
        self.assertEqual(review.title, "Updated")
        self.assertFalse(review.is_approved)

    def test_a_user_cannot_edit_someone_elses_review(self):
        review = Review.objects.create(
            product=self.product, user=self.buyer, rating=4, title="Original", body="Ok.",
        )
        self.client.login(username="nonbuyer", password="testpass123")
        response = self.client.post(
            reverse("products:edit_review", args=[review.id]),
            {"rating": 1, "title": "Hijacked", "body": "Not theirs."},
        )
        self.assertEqual(response.status_code, 404)
        review.refresh_from_db()
        self.assertEqual(review.title, "Original")

    def test_owner_can_delete_their_own_review(self):
        self.client.login(username="buyer", password="testpass123")
        review = Review.objects.create(product=self.product, user=self.buyer, rating=4, title="x", body="x")
        self.client.post(reverse("products:delete_review", args=[review.id]))
        self.assertEqual(Review.objects.count(), 0)


class ReviewModerationViewTests(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name="Homeware")
        self.product = Product.objects.create(
            category=self.category, name="Rug", description="x", price=Decimal("30.00"),
        )
        self.reviewer = User.objects.create_user(username="reviewer", password="testpass123")
        self.staff_user = User.objects.create_user(username="staffer", password="testpass123", is_staff=True)
        self.regular_user = User.objects.create_user(username="regular", password="testpass123")
        self.review = Review.objects.create(
            product=self.product, user=self.reviewer, rating=3, title="Pending", body="Awaiting approval.",
        )

    def test_non_staff_user_gets_403(self):
        self.client.login(username="regular", password="testpass123")
        response = self.client.get(reverse("products:review_moderation"))
        self.assertEqual(response.status_code, 403)

    def test_anonymous_user_gets_403(self):
        response = self.client.get(reverse("products:review_moderation"))
        self.assertEqual(response.status_code, 403)

    def test_staff_user_can_view_the_moderation_queue(self):
        self.client.login(username="staffer", password="testpass123")
        response = self.client.get(reverse("products:review_moderation"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Pending")

    def test_staff_can_approve_a_review(self):
        self.client.login(username="staffer", password="testpass123")
        self.client.post(reverse("products:approve_review", args=[self.review.id]))
        self.review.refresh_from_db()
        self.assertTrue(self.review.is_approved)

    def test_staff_can_reject_and_delete_a_review(self):
        self.client.login(username="staffer", password="testpass123")
        self.client.post(reverse("products:reject_review", args=[self.review.id]))
        self.assertEqual(Review.objects.count(), 0)


class StaffProductManagementTests(TestCase):

    """ Covers issue #29: managing products and categories from the
    front end, without the Django admin, including the safeguard
    against deleting a product or category tied to real order
    history. """

    def setUp(self):
        self.category = Category.objects.create(name="Ankara Fabrics")
        self.product = Product.objects.create(
            category=self.category, name="Test Print", description="x", price=Decimal("20.00"),
        )
        self.staff_user = User.objects.create_user(username="staffer", password="testpass123", is_staff=True)
        self.regular_user = User.objects.create_user(username="shopper", password="testpass123")

    def test_non_staff_cannot_reach_the_product_list(self):
        self.client.login(username="shopper", password="testpass123")
        response = self.client.get(reverse("products:staff_product_list"))
        self.assertEqual(response.status_code, 403)

    def test_staff_can_view_the_product_list(self):
        self.client.login(username="staffer", password="testpass123")
        response = self.client.get(reverse("products:staff_product_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Print")

    def test_staff_can_add_a_product_with_no_images_or_variants(self):
        self.client.login(username="staffer", password="testpass123")
        self.client.post(reverse("products:staff_product_add"), {
            "category": self.category.id, "name": "Brand New Print", "description": "x",
            "price": "18.00", "stock_quantity": 5, "is_featured": False, "is_active": True,
            "images-TOTAL_FORMS": "0", "images-INITIAL_FORMS": "0",
            "images-MIN_NUM_FORMS": "0", "images-MAX_NUM_FORMS": "1000",
            "variants-TOTAL_FORMS": "0", "variants-INITIAL_FORMS": "0",
            "variants-MIN_NUM_FORMS": "0", "variants-MAX_NUM_FORMS": "1000",
        })
        self.assertTrue(Product.objects.filter(name="Brand New Print").exists())

    def test_image_and_variant_formsets_do_not_collide_when_their_row_counts_differ(self):

        """ Regression test for a real bug found while building this
        suite: both formsets defaulted to the same prefix ("form"),
        so submitting a different number of images than variants
        made the browser send two different values for the same
        hidden management-form field, and only one of them actually
        reached each formset, silently dropping whichever rows sat
        past the shorter count. Explicit, distinct prefixes
        (build_image_formset / build_variant_formset in
        products/forms.py) fix this - this test adds two images and
        one variant in a single submission and checks both are
        fully saved, not just whichever one happened to match. """

        image_one = SimpleUploadedFile("front.gif", TINY_GIF, content_type="image/gif")
        image_two = SimpleUploadedFile("back.gif", TINY_GIF, content_type="image/gif")

        self.client.login(username="staffer", password="testpass123")
        self.client.post(reverse("products:staff_product_add"), {
            "category": self.category.id, "name": "Two Images One Variant", "description": "x",
            "price": "22.00", "stock_quantity": 5, "is_featured": False, "is_active": True,
            "images-TOTAL_FORMS": "2", "images-INITIAL_FORMS": "0",
            "images-MIN_NUM_FORMS": "0", "images-MAX_NUM_FORMS": "1000",
            "images-0-image": image_one, "images-0-alt_text": "Front view", "images-0-is_primary": "on",
            "images-1-image": image_two, "images-1-alt_text": "Back view",
            "variants-TOTAL_FORMS": "1", "variants-INITIAL_FORMS": "0",
            "variants-MIN_NUM_FORMS": "0", "variants-MAX_NUM_FORMS": "1000",
            "variants-0-variant_type": "size", "variants-0-value": "Medium",
            "variants-0-stock_quantity": "5", "variants-0-price_adjustment": "0",
        })
        product = Product.objects.get(name="Two Images One Variant")
        self.assertEqual(product.images.count(), 2)
        self.assertEqual(product.variants.count(), 1)

    def test_staff_can_toggle_a_product_inactive_and_active_again(self):
        self.client.login(username="staffer", password="testpass123")
        self.client.post(reverse("products:staff_product_toggle_active", args=[self.product.slug]))
        self.product.refresh_from_db()
        self.assertFalse(self.product.is_active)
        self.client.post(reverse("products:staff_product_toggle_active", args=[self.product.slug]))
        self.product.refresh_from_db()
        self.assertTrue(self.product.is_active)

    def test_a_never_ordered_product_can_be_deleted(self):
        self.client.login(username="staffer", password="testpass123")
        self.client.post(reverse("products:staff_product_delete", args=[self.product.slug]))
        self.assertFalse(Product.objects.filter(id=self.product.id).exists())

    def test_a_product_with_order_history_cannot_be_deleted(self):
        buyer = User.objects.create_user(username="buyer2", password="testpass123")
        order = Order.objects.create(
            user=buyer, full_name="Buyer", email="buyer2@example.com", phone_number="123",
            address_line1="1 Test St", town_or_city="Testville", postcode="12345", country="IE",
        )
        OrderLineItem.objects.create(
            order=order, product=self.product, quantity=1, price_at_purchase=Decimal("20.00"),
        )
        self.client.login(username="staffer", password="testpass123")
        self.client.post(reverse("products:staff_product_delete", args=[self.product.slug]))
        self.assertTrue(Product.objects.filter(id=self.product.id).exists())

    def test_a_category_with_products_cannot_be_deleted(self):
        self.client.login(username="staffer", password="testpass123")
        self.client.post(reverse("products:staff_category_delete", args=[self.category.slug]))
        self.assertTrue(Category.objects.filter(id=self.category.id).exists())

    def test_an_empty_category_can_be_deleted(self):
        empty_category = Category.objects.create(name="Temporary")
        self.client.login(username="staffer", password="testpass123")
        self.client.post(reverse("products:staff_category_delete", args=[empty_category.slug]))
        self.assertFalse(Category.objects.filter(id=empty_category.id).exists())