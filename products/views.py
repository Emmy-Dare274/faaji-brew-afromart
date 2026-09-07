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


def product_detail(request, product_slug):

    """ Shows full details for one product: images, variants, price,
    and its current rating. Individual reviews are not listed yet. """

    product = get_object_or_404(
        Product.objects.with_rating(), slug=product_slug, is_active=True
    )
    variants = product.variants.all().order_by("variant_type", "value")
    context = {
        "product": product,
        "variants": variants,
    }
    return render(request, "products/product_detail.html", context)


def category_overview(request):

    """The dedicated page the 'Category' nav item points to, kept
    separate from the homepage's own category rail so it can grow
    on its own later without touching the homepage."""

    categories = Category.objects.active()
    return render(request, "products/category_overview.html", {"categories": categories})


def special_offers(request):

    """A shuffled, discovery-style listing rather than a fixed
    curated one. Narrowing to a category (from the navbar dropdown)
    keeps the same random order, just scoped to that category."""
    
    products = Product.objects.filter(is_active=True).with_rating().order_by("?")
    selected_category = None
    category_slug = request.GET.get("category")
    if category_slug:
        selected_category = get_object_or_404(Category, slug=category_slug, is_active=True)
        products = products.filter(category=selected_category)

    context = {
        "category": selected_category,
        "products": products,
        "all_categories": Category.objects.active(),
        "query": "", "min_price": "", "max_price": "", "current_sort": "",
        "product_count": products.count(),
        "page_title": f"{selected_category.name} Special Offers" if selected_category else "Special Offers",
    }
    return render(request, "products/product_list.html", context)

