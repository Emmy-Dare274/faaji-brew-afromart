from django.core import mail
from django.test import TestCase
from django.urls import reverse

from products.models import Category, Product


class StaticPageTests(TestCase):

    """ Covers issue #30 (every page reachable and working) and
    issue #32 (every page renders with its own real template). """

    def test_home_page_loads(self):
        response = self.client.get(reverse("core:home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/home.html")

    def test_home_page_context_includes_categories_and_featured_products(self):
        category = Category.objects.create(name="Ankara Fabrics")
        Product.objects.create(
            category=category, name="Test Fabric", description="A test product.",
            price=25, is_featured=True, is_active=True,
        )
        response = self.client.get(reverse("core:home"))
        self.assertIn("categories", response.context)
        self.assertIn("featured_products", response.context)
        self.assertEqual(response.context["featured_products"].count(), 1)

    def test_our_story_page_loads(self):
        response = self.client.get(reverse("core:our_story"))
        self.assertEqual(response.status_code, 200)

    def test_terms_of_use_page_loads(self):
        response = self.client.get(reverse("core:terms_of_use"))
        self.assertEqual(response.status_code, 200)

    def test_privacy_policy_page_loads(self):
        response = self.client.get(reverse("core:privacy_policy"))
        self.assertEqual(response.status_code, 200)

    def test_delivery_returns_page_loads(self):
        response = self.client.get(reverse("core:delivery_returns"))
        self.assertEqual(response.status_code, 200)

    def test_faq_page_loads(self):
        response = self.client.get(reverse("core:faq"))
        self.assertEqual(response.status_code, 200)


class RobotsTxtTests(TestCase):

    """ Covers issue #37: a working robots.txt that names the
    sitemap using whatever host actually served the request. """

    def test_robots_txt_is_plain_text_and_names_the_sitemap(self):
        response = self.client.get(reverse("core:robots_txt"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "text/plain")
        self.assertIn("Sitemap:", response.content.decode())


class ContactFormTests(TestCase):

    """ Covers issue #36: a real, working contact form that sends
    an actual email rather than just showing a success message. """

    def test_contact_page_loads(self):
        response = self.client.get(reverse("core:contact_us"))
        self.assertEqual(response.status_code, 200)

    def test_valid_submission_sends_an_email_and_redirects(self):
        response = self.client.post(reverse("core:contact_us"), {
            "name": "Jane Shopper",
            "email": "jane@example.com",
            "message": "Do you ship to Ireland?",
        })
        self.assertRedirects(response, reverse("core:contact_us"))
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("Jane Shopper", mail.outbox[0].subject)
        self.assertEqual(mail.outbox[0].reply_to, ["jane@example.com"])

    def test_missing_message_shows_the_form_again_without_sending_an_email(self):
        response = self.client.post(reverse("core:contact_us"), {
            "name": "Jane Shopper",
            "email": "jane@example.com",
            "message": "",
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(mail.outbox), 0)
        self.assertTrue(response.context["form"].errors)