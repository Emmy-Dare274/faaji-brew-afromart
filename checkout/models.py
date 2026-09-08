import uuid
from decimal import Decimal

from django.conf import settings
from django.db import models
from django_countries.fields import CountryField

from products.models import Product, ProductVariant
from basket.models import FREE_DELIVERY_THRESHOLD, STANDARD_DELIVERY_COST


class Order(models.Model):
    """An order can only belong to a real user, never a guest,
    that's what actually enforces 'registration required at
    checkout' in the database."""

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        PROCESSING = "processing", "Processing"
        SHIPPED = "shipped", "Shipped"
        DELIVERED = "delivered", "Delivered"
        CANCELLED = "cancelled", "Cancelled"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders"
    )
    order_number = models.CharField(max_length=32, unique=True, editable=False)
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.PENDING)

    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=30)
    address_line1 = models.CharField(max_length=150)
    address_line2 = models.CharField(max_length=150, blank=True)
    town_or_city = models.CharField(max_length=100)
    postcode = models.CharField(max_length=20)
    country = CountryField(blank_label="Select country")

    order_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    delivery_cost = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    stripe_pid = models.CharField(max_length=254, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.order_number

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = uuid.uuid4().hex.upper()
        super().save(*args, **kwargs)

    def update_totals(self):
        """The one place order totals get calculated. Both the
        checkout view (when the order is first created) and the
        Stripe webhook (once payment is confirmed) call this same
        method. Decimal is used throughout, deliberately not float, since 
        mixing the two in real money calculations risks the kind of silent 
        rounding errors floats are known for."""

        self.order_total = sum(
            (item.lineitem_total for item in self.lineitems.all()), Decimal("0.00")
        )
        self.delivery_cost = Decimal("0.00") if self.order_total >= FREE_DELIVERY_THRESHOLD else STANDARD_DELIVERY_COST
        self.grand_total = self.order_total + self.delivery_cost
        self.save(update_fields=["order_total", "delivery_cost", "grand_total"])


class OrderLineItem(models.Model):
    """price_at_purchase is deliberately copied from the product at
    checkout time rather than always reading the live product price.
    If a product's price changes next time, past orders must still
    reflect what the customer actually paid, not today's price."""

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="lineitems")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variant = models.ForeignKey(ProductVariant, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField()
    price_at_purchase = models.DecimalField(max_digits=8, decimal_places=2)

    @property
    def lineitem_total(self):
        if self.price_at_purchase is None or self.quantity is None:
            return 0
        return self.price_at_purchase * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.product.name} on order {self.order.order_number}"