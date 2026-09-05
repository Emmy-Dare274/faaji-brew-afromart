from django.shortcuts import render, get_object_or_404
from .models import Category, Product


def product_list(request, category_slug=None):

    """ Shows every active product, optionally filtered to one
    category. """

    category = None
    products = Product.objects.filter(is_active=True).with_rating()

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug, is_active=True)
        products = products.filter(category=category)

    context = {
        "category": category,
        "products": products,
    }
    return render(request, "products/product_list.html", context)
