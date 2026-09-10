from django.http import HttpResponse
from django.core.mail import send_mail

from .models import Order


class StripeWH_Handler:
    """Each Stripe event type this app cares about gets its own
    handler method here, kept separate from views.py."""

    def __init__(self, request):
        self.request = request

    def handle_event(self, event):
        """Anything Stripe sends that this app has no specific
        handler for is simply acknowledged, not treated as an
        error."""
        return HttpResponse(content=f"Unhandled webhook received: {event['type']}", status=200)

    def handle_payment_intent_succeeded(self, event):
        # .to_dict() converts Stripe's own object type into a real
        # Python dictionary, so ordinary dict methods like .get()
        # actually work correctly on everything nested inside it,
        # metadata included.
        intent = event["data"]["object"].to_dict()
        order_number = intent.get("metadata", {}).get("order_number")

        try:
            order = Order.objects.get(order_number=order_number)
        except Order.DoesNotExist:
            return HttpResponse(content=f"Order {order_number} not found", status=200)

        # Stripe can deliver the same successful-payment event more
        # than once. Only acting while the order is still pending is
        # what stops a customer receiving two confirmation emails
        # for one real payment.
        if order.status == Order.Status.PENDING:
            order.status = Order.Status.PROCESSING
            order.save(update_fields=["status"])
            self._send_confirmation_email(order)

        return HttpResponse(
            content=f"Webhook received: {event['type']} | order {order.order_number} confirmed",
            status=200,
        )

    def _send_confirmation_email(self, order):
        lines = [f"Thank you for your order, {order.full_name}.", ""]
        for item in order.lineitems.all():
            lines.append(f"{item.quantity} x {item.product.name} - ${item.lineitem_total:.2f}")
        lines += [
            "",
            f"Order total: ${order.order_total:.2f}",
            f"Delivery: ${order.delivery_cost:.2f}",
            f"Grand total: ${order.grand_total:.2f}",
            "",
            f"Delivering to: {order.address_line1}, {order.town_or_city}, "
            f"{order.postcode}, {order.country.name}",
        ]
        send_mail(
            subject=f"Your Faaji & Brew AfroMart Shopping order {order.order_number}",
            message="\n".join(lines),
            from_email=None,
            recipient_list=[order.email],
        )
