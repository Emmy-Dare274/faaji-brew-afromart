from django.core import mail
from django.test import TestCase
from django.urls import reverse

from .forms import NewsletterSignupForm
from .models import NewsletterSubscriber


class NewsletterSubscriberModelTests(TestCase):

    def test_string_representation_is_the_email(self):
        subscriber = NewsletterSubscriber.objects.create(email="jane@example.com")
        self.assertEqual(str(subscriber), "jane@example.com")


class NewsletterSignupFormTests(TestCase):

    def test_valid_email_is_accepted(self):
        form = NewsletterSignupForm(data={"email": "jane@example.com"})
        self.assertTrue(form.is_valid())

    def test_invalid_email_is_rejected(self):
        form = NewsletterSignupForm(data={"email": "not-an-email"})
        self.assertFalse(form.is_valid())


class NewsletterSignupViewTests(TestCase):

    """ Covers the homepage newsletter signup: a real confirmation
    email rather than an immediate, unverified subscription. """

    def test_valid_email_creates_an_unconfirmed_subscriber_and_sends_an_email(self):
        response = self.client.post(
            reverse("marketing:newsletter_signup"), {"email": "jane@example.com"}
        )
        subscriber = NewsletterSubscriber.objects.get(email="jane@example.com")
        self.assertFalse(subscriber.confirmed)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn(str(subscriber.confirmation_token), mail.outbox[0].body)
        self.assertRedirects(response, reverse("core:home"))

    def test_invalid_email_does_not_create_a_subscriber_or_send_an_email(self):
        self.client.post(reverse("marketing:newsletter_signup"), {"email": "not-an-email"})
        self.assertEqual(NewsletterSubscriber.objects.count(), 0)
        self.assertEqual(len(mail.outbox), 0)

    def test_an_already_confirmed_email_is_not_signed_up_again(self):
        NewsletterSubscriber.objects.create(email="jane@example.com", confirmed=True)
        self.client.post(reverse("marketing:newsletter_signup"), {"email": "jane@example.com"})
        self.assertEqual(NewsletterSubscriber.objects.count(), 1)
        self.assertEqual(len(mail.outbox), 0)

    def test_an_already_pending_email_does_not_get_a_second_confirmation_email(self):
        NewsletterSubscriber.objects.create(email="jane@example.com", confirmed=False)
        self.client.post(reverse("marketing:newsletter_signup"), {"email": "jane@example.com"})
        self.assertEqual(NewsletterSubscriber.objects.count(), 1)
        self.assertEqual(len(mail.outbox), 0)

    def test_redirects_to_the_provided_next_url_when_given(self):
        response = self.client.post(reverse("marketing:newsletter_signup"), {
            "email": "jane@example.com", "next": reverse("products:product_list"),
        })
        self.assertRedirects(response, reverse("products:product_list"))


class ConfirmSubscriptionViewTests(TestCase):

    def test_a_valid_token_confirms_the_subscription(self):
        subscriber = NewsletterSubscriber.objects.create(email="jane@example.com")
        self.client.get(
            reverse("marketing:confirm_subscription", args=[subscriber.confirmation_token])
        )
        subscriber.refresh_from_db()
        self.assertTrue(subscriber.confirmed)

    def test_an_unknown_token_returns_404(self):
        response = self.client.get(
            reverse(
                "marketing:confirm_subscription",
                args=["11111111-1111-1111-1111-111111111111"],
            )
        )
        self.assertEqual(response.status_code, 404)
