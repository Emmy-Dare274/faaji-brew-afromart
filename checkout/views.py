import stripe
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import prefetch_related_objects
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .webhook_handler import StripeWH_Handler

from basket.services import get_or_create_basket
from profiles.models import UserProfile
from .forms import OrderForm
from .models import Order
from .services import create_order_from_basket

stripe.api_key = settings.STRIPE_SECRET_KEY


@login_required
def checkout(request):
    """Login is required for this view, that is what
    actually enforces registration at checkout, not just a UI
    suggestion."""
    basket = get_or_create_basket(request)
    prefetch_related_objects([basket], "items__product__images", "items__variant")

    if not basket.items.exists():
        messages.error(request, "Your basket is empty, add something before checking out.")
        return redirect("products:product_list")

    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            order = create_order_from_basket(request.user, basket, form.cleaned_data)

            UserProfile.objects.update_or_create(
                user=request.user,
                defaults={
                    "default_full_name": form.cleaned_data["full_name"],
                    "default_phone_number": form.cleaned_data["phone_number"],
                    "default_address_line1": form.cleaned_data["address_line1"],
                    "default_address_line2": form.cleaned_data["address_line2"],
                    "default_town_or_city": form.cleaned_data["town_or_city"],
                    "default_postcode": form.cleaned_data["postcode"],
                    "default_country": form.cleaned_data["country"],
                },
            )

            intent = stripe.PaymentIntent.create(
                amount=int(order.grand_total * 100),
                currency="usd",
                metadata={"order_number": order.order_number},
            )
            order.stripe_pid = intent.id
            order.save(update_fields=["stripe_pid"])

            context = {
                "order": order,
                "client_secret": intent.client_secret,
                "stripe_public_key": settings.STRIPE_PUBLIC_KEY,
            }
            return render(request, "checkout/checkout_payment.html", context)
        messages.error(request, "Please correct the errors below.")
    else:
        initial = {"email": request.user.email, "full_name": request.user.username}
        try:
            profile = request.user.profile
            initial.update({
                "full_name": profile.default_full_name or request.user.username,
                "phone_number": profile.default_phone_number,
                "address_line1": profile.default_address_line1,
                "address_line2": profile.default_address_line2,
                "town_or_city": profile.default_town_or_city,
                "postcode": profile.default_postcode,
                "country": profile.default_country,
            })
        except UserProfile.DoesNotExist:
            pass
        form = OrderForm(initial=initial)

    return render(request, "checkout/checkout.html", {"form": form, "basket": basket})


@login_required
def checkout_success(request, order_number):
    order = get_object_or_404(Order, order_number=order_number, user=request.user)

    # The basket is cleared here, right after Stripe confirms success
    # in the customer's browser. Next session's webhook becomes the
    # real, server-side source of truth, since a browser
    # that loses connection right after payment would otherwise
    # never reach this view at all despite having actually paid.
    basket = get_or_create_basket(request)
    basket.items.all().delete()

    messages.success(request, f"Order successfully placed. Your order number is {order.order_number}.")
    return render(request, "checkout/checkout_success.html", {"order": order})


@csrf_exempt
def webhook(request):
    """Stripe posts here directly, with no CSRF token."""
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, settings.STRIPE_WEBHOOK_SECRET)
    except ValueError:
        return HttpResponse(status=400)
    except stripe.SignatureVerificationError:
        return HttpResponse(status=400)

    handler = StripeWH_Handler(request)
    event_map = {
        "payment_intent.succeeded": handler.handle_payment_intent_succeeded,
    }
    event_handler = event_map.get(event["type"], handler.handle_event)
    return event_handler(event)