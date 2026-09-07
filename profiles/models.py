from django.db import models
from django.conf import settings
from products.models import Product


class WishList(models.Model):
    
    """One favourites list per registered user. Saving requires
    being logged in, unlike the basket, since a favourites list tied
    only to a browser session would not be very useful."""

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="wishlist")

    def __str__(self):
        return f"Wishlist for {self.user.username}"


class WishListItem(models.Model):
    wishlist = models.ForeignKey(WishList, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["wishlist", "product"]
        ordering = ["-added_at"]

    def __str__(self):
        return f"{self.product.name} in {self.wishlist}"