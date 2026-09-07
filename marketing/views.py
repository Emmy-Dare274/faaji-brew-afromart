from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.decorators.http import require_POST

from .forms import NewsletterSignupForm
from .models import NewsletterSubscriber


@require_POST
def newsletter_signup(request):
    email = request.POST.get("email", "").strip()
    next_url = request.POST.get("next") or "core:home"

    existing = NewsletterSubscriber.objects.filter(email__iexact=email).first()
    if existing:
        message = "You're already subscribed, thanks for being here." if existing.confirmed \
            else "You're already signed up, check your inbox to confirm."
        messages.info(request, message)
        return redirect(next_url)

    form_data = request.POST.copy()
    form_data["email"] = email
    form = NewsletterSignupForm(form_data)
    if not form.is_valid():
        messages.error(request, "Please enter a valid email address.")
        return redirect(next_url)

    subscriber = form.save()
    confirm_url = request.build_absolute_uri(
        reverse("marketing:confirm_subscription", args=[subscriber.confirmation_token])
    )
    send_mail(
        subject="Confirm your F&B AfroMart newsletter subscription",
        message=f"Thanks for signing up. Confirm your subscription here: {confirm_url}",
        from_email=None,
        recipient_list=[subscriber.email],
    )
    messages.success(request, "Almost there, check your inbox to confirm your subscription.")
    return redirect(next_url)


def confirm_subscription(request, token):
    subscriber = get_object_or_404(NewsletterSubscriber, confirmation_token=token)
    subscriber.confirmed = True
    subscriber.save(update_fields=["confirmed"])
    messages.success(request, "Subscription confirmed. Welcome to the F&B AfroMart newsletter.")
    return redirect("core:home")