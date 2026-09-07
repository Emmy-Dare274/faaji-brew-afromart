import stripe
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from basket.services import get_or_create_basket
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

    if not basket.items.exists():
        messages.error(request, "Your basket is empty, add something before checking out.")
        return redirect("products:product_list")

    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            order = create_order_from_basket(request.user, basket, form.cleaned_data)

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
        form = OrderForm(initial={"email": request.user.email, "full_name": request.user.username})

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