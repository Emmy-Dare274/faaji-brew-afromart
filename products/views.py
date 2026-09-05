from django.shortcuts import render, get_object_or_404
from .models import Category, Product


def product_list(request, category_slug=None):
    """ Shows every active product, optionally filtered by category,
    keyword, price range, and sorted by the chosen field."""

    category = None
    products = Product.objects.filter(is_active=True).with_rating()

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug, is_active=True)
        products = products.filter(category=category)

    query = request.GET.get("q", "")
    if query:
        products = products.search(query)

    min_price = request.GET.get("min_price", "")
    max_price = request.GET.get("max_price", "")
    if min_price or max_price:
        products = products.price_range(min_price or None, max_price or None)

    sort = request.GET.get("sort", "")
    sort_fields = {
        "price_asc": "price",
        "price_desc": "-price",
        "rating_asc": "average_rating",
        "rating_desc": "-average_rating",
        "name_asc": "name",
        "name_desc": "-name",
        "category_asc": "category__name",
        "category_desc": "-category__name",
    }
    if sort in sort_fields:
        products = products.order_by(sort_fields[sort])

    context = {
        "category": category,
        "products": products,
        "all_categories": Category.objects.active(),
        "query": query,
        "min_price": min_price,
        "max_price": max_price,
        "current_sort": sort,
        "product_count": products.count(),
    }
    return render(request, "products/product_list.html", context)
