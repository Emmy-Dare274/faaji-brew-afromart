import random
from pathlib import Path

from django.contrib.auth import get_user_model
from django.core.files import File
from django.core.management.base import BaseCommand
from django.db import transaction

from products.models import Category, Product, ProductImage, ProductVariant, Review
from products.seed_data import CATEGORIES, PRODUCTS, REVIEWER_USERNAMES, REVIEW_POOL

SEED_IMAGES_DIR = Path(__file__).resolve().parent.parent.parent.parent / "seed_images"


class Command(BaseCommand):
    help = (
        "Creates categories and products from products/seed_data.py, "
        "uploading each image to Cloudinary through the ORM, and seeds "
        "placeholder ratings and sales figures. Safe to re-run: existing "
        "products are matched by name and only backfilled, not duplicated."
    )

    def handle(self, *args, **options):
        with transaction.atomic():
            self._seed_categories()
            self.reviewers = self._get_or_create_reviewers()
            self._seed_products()

    def _seed_categories(self):
        for cat_data in CATEGORIES:
            category, created = Category.objects.get_or_create(
                name=cat_data["name"],
                defaults={"description": cat_data.get("description", "")},
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created category: {category.name}"))

    def _get_or_create_reviewers(self):
        # These accounts exist purely to attach realistic-looking seed
        # reviews to a pre-launch catalogue. They can never log in,
        # set_unusable_password makes that explicit.
        User = get_user_model()
        users = []
        for username in REVIEWER_USERNAMES:
            user, created = User.objects.get_or_create(
                username=username, defaults={"email": f"{username}@example.com"}
            )
            if created:
                user.set_unusable_password()
                user.save()
            users.append(user)
        return users

    def _seed_products(self):
        for prod_data in PRODUCTS:
            category = Category.objects.get(name=prod_data["category"])
            product, created = Product.objects.get_or_create(
                name=prod_data["name"],
                defaults={
                    "category": category,
                    "description": prod_data["description"],
                    "price": prod_data["price"],
                    "stock_quantity": prod_data.get("stock_quantity", 20),
                    "is_featured": prod_data.get("is_featured", False),
                },
            )

            if created:
                for index, filename in enumerate(prod_data.get("images", [])):
                    self._attach_product_image(product, filename, is_primary=(index == 0))
                for variant in prod_data.get("variants", []):
                    ProductVariant.objects.create(
                        product=product,
                        variant_type=variant["type"],
                        value=variant["value"],
                        stock_quantity=variant.get("stock_quantity", 10),
                    )
                self.stdout.write(self.style.SUCCESS(f"Created product: {product.name}"))
            else:
                self.stdout.write(f"Product already exists, checking for missing seed data: {product.name}")

            # Backfilled here rather than only in defaults, so products
            # created before this field existed still get a value when
            # the command is re-run, not just brand new ones.
            if product.units_sold == 0:
                product.units_sold = random.randint(15, 420)
                product.save(update_fields=["units_sold"])

            self._maybe_seed_reviews(product)

    def _maybe_seed_reviews(self, product):
        # Roughly 90 percent of products get seeded with placeholder
        # ratings so the catalogue does not look empty pre-launch.
        # This is clearly-marked seed data, not real customer
        # feedback, and is entirely separate from the real review
        # system regular users will submit through going forward.
        if random.random() > 0.9:
            return
        review_count = random.randint(1, 3)
        chosen_reviewers = random.sample(self.reviewers, min(review_count, len(self.reviewers)))
        for reviewer in chosen_reviewers:
            rating = random.randint(3, 5)
            title, body = random.choice(REVIEW_POOL[rating])
            Review.objects.get_or_create(
                product=product, user=reviewer,
                defaults={"rating": rating, "title": title, "body": body, "is_approved": True},
            )

    def _attach_product_image(self, product, filename, is_primary=False):
        path = SEED_IMAGES_DIR / filename
        if not path.exists():
            self.stdout.write(self.style.WARNING(f"Missing image, skipping: {filename}"))
            return
        with open(path, "rb") as f:
            image = ProductImage(product=product, is_primary=is_primary)
            image.image.save(filename, File(f), save=True)