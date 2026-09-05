from django.shortcuts import render
from products.models import Category, Product


def home(request):

    """ Renders the homepage. Pulls categories and featured
    products now that the products app has models to query. """

    categories = Category.objects.active()
    featured_products = Product.objects.featured().with_rating()[:4]
    context = {
        "categories": categories,
        "featured_products": featured_products,
    }
    return render(request, "core/home.html", context)
