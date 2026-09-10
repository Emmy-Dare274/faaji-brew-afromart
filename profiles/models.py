from django.db import models
from django.conf import settings
from django_countries.fields import CountryField
from products.models import Product


class UserProfile(models.Model):

    """ Saved default delivery details, so a returning customer
    doesn't have to retype their address at every checkout. Filled
    in automatically the first time someone completes an order, and
    editable any time from My Account. """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile"
    )
    default_full_name = models.CharField(max_length=100, blank=True)
    default_phone_number = models.CharField(max_length=30, blank=True)
    default_address_line1 = models.CharField(max_length=150, blank=True)
    default_address_line2 = models.CharField(max_length=150, blank=True)
    default_town_or_city = models.CharField(max_length=100, blank=True)
    default_postcode = models.CharField(max_length=20, blank=True)
    default_country = CountryField(blank=True, blank_label="Select country")

    def __str__(self):
        return f"Profile for {self.user.username}"


class WishList(models.Model):

    """One favourites list per registered user. Saving requires
    being logged in, unlike the basket, since a favourites list tied
    only to a browser session would not be very useful."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="wishlist"
    )

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
