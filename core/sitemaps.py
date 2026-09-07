from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from products.models import Category, Product


class StaticViewSitemap(Sitemap):

    """ Fixed pages that don't come from a model: the homepage, the
    brand story, the category and special offers landing pages, and
    the two legal pages. Listed by URL name so adding a new static
    page later is a one-line change here, not a new class. """

    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return [
            "core:home",
            "core:our_story",
            "core:terms_of_use",
            "core:privacy_policy",
            "products:category_overview",
            "products:special_offers",
        ]

    def location(self, item):
        return reverse(item)


class CategorySitemap(Sitemap):

    """ One entry per active shop category, so each category listing
    page is independently discoverable rather than only reachable by
    following a link from the homepage. """

    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return Category.objects.active()

    def location(self, obj):
        return reverse("products:product_list_by_category", args=[obj.slug])


class ProductSitemap(Sitemap):

    """ One entry per active product. lastmod comes straight from the
    model's own updated_at field, so search engines see exactly when
    a listing last changed without any extra bookkeeping. """

    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Product.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return reverse("products:product_detail", args=[obj.slug])
