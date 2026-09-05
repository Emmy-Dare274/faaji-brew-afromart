from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator


class Category(models.Model):
    """A shop category, for example Ankara Fabrics or Spices and Sauce
    Kits. Managed through the Django admin for now. A front end staff
    management page comes later, once the basic catalogue works."""

    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=110, unique=True, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="categories/", blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Auto generates the slug from the name, so staff never have
        # to type one by hand when adding a category in the admin.
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class ProductQuerySet(models.QuerySet):
    """Queries used in more than one place across the site live here,
    once, instead of being repeated in every view that needs them. """

    def in_stock(self):
        return self.filter(stock_quantity__gt=0)

    def featured(self):
        return self.filter(is_featured=True, is_active=True)

    def by_category(self, slug):
        return self.filter(category__slug=slug, is_active=True)

    def with_rating(self):
        # Attaches an average_rating value to each product, calculated
        # only from reviews that have been approved by staff.
        return self.annotate(
            average_rating=models.Avg(
                "reviews__rating",
                filter=models.Q(reviews__is_approved=True),
            )
        )


class Product(models.Model):
    """A single sellable item. Size and colour options live in their
    own ProductVariant model below, not as fields here, since one
    product can have several variants, each with its own stock."""

    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="products"
    )
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=210, unique=True, blank=True)
    sku = models.CharField(max_length=30, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    stock_quantity = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ProductQuerySet.as_manager()

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def in_stock(self):
        return self.stock_quantity > 0


class ProductImage(models.Model):
    """More than one photo per product. """

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(upload_to="products/")
    alt_text = models.CharField(max_length=150, blank=True)
    is_primary = models.BooleanField(default=False)

    def __str__(self):
        return f"Image for {self.product.name}"


class ProductVariant(models.Model):
    """A specific size or colour option, each with its own stock
    count."""

    class VariantType(models.TextChoices):
        SIZE = "size", "Size"
        COLOUR = "colour", "Colour"

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="variants"
    )
    variant_type = models.CharField(max_length=10, choices=VariantType.choices)
    value = models.CharField(max_length=50)
    stock_quantity = models.PositiveIntegerField(default=0)
    price_adjustment = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    class Meta:
        unique_together = ["product", "variant_type", "value"]

    def __str__(self):
        return f"{self.product.name} - {self.value}"


class Review(models.Model):
    """A customer review. Approved, featured reviews."""

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="reviews"
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    title = models.CharField(max_length=120)
    body = models.TextField()
    is_approved = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        unique_together = ["product", "user"]

    def __str__(self):
        return f"{self.rating} star review for {self.product.name}"