from django.db import models
from django.conf import settings
from products.models import Product, ProductVariant
from decimal import Decimal

FREE_DELIVERY_THRESHOLD = Decimal("60.00")
STANDARD_DELIVERY_COST = Decimal("4.99")


class Basket(models.Model):

    """ A shopping basket. Tied to a logged-in user once they exist,
    or to an anonymous session key before that, so browsing and
    building a basket works without an account. Checkout itself
    still requires logging in, that rule lives in the checkout app,
    not here. """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        null=True, blank=True, related_name="baskets",
    )
    session_key = models.CharField(max_length=40, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        owner = self.user.username if self.user else f"guest ({self.session_key})"
        return f"Basket for {owner}"

    @property
    def total(self):
        return sum(item.line_total for item in self.items.all())

    @property
    def item_count(self):
        return sum(item.quantity for item in self.items.all())

    @property
    def amount_to_free_delivery(self):
        remaining = FREE_DELIVERY_THRESHOLD - self.total
        return remaining if remaining > 0 else Decimal("0.00")

    @property
    def qualifies_for_free_delivery(self):
        return self.total >= FREE_DELIVERY_THRESHOLD


class BasketItem(models.Model):

    """ One product, and optional variant, sitting in a basket with a
    quantity. A database model which gives us a genuine front end
    delete action later without touching the admin panel. """

    basket = models.ForeignKey(Basket, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variant = models.ForeignKey(
        ProductVariant, on_delete=models.CASCADE, null=True, blank=True
    )
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ["basket", "product", "variant"]

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    @property
    def unit_price(self):
        price = self.product.price
        if self.variant:
            price += self.variant.price_adjustment
        return price

    @property
    def line_total(self):
        return self.unit_price * self.quantity
