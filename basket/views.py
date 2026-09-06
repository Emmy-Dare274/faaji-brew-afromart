from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from products.models import Product, ProductVariant
from .services import get_or_create_basket, add_item, update_quantity


def basket_detail(request):
    basket = get_or_create_basket(request)
    return render(request, "basket/basket_detail.html", {"basket": basket})


@require_POST
def add_to_basket(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug, is_active=True)
    quantity = int(request.POST.get("quantity", 1))
    variant_id = request.POST.get("variant_id")
    variant = (
        get_object_or_404(ProductVariant, id=variant_id, product=product)
        if variant_id else None
    )

    # Defensive check: never let a basket claim more stock than
    # actually exists, whether that is a genuine mistake or someone
    # tampering with the form directly.

    available = variant.stock_quantity if variant else product.stock_quantity
    if quantity < 1 or available < quantity:
        messages.error(request, f"Sorry, only {available} of {product.name} left in stock.")
        return redirect("products:product_detail", product_slug=product.slug)

    basket = get_or_create_basket(request)
    add_item(basket, product, variant, quantity)
    messages.success(request, f"Added {product.name} to your basket.")
    return redirect("basket:basket_detail")


@require_POST
def update_basket_item(request, item_id):
    basket = get_or_create_basket(request)
    # Looking the item up through basket.items, not BasketItem
    # directly, stops someone editing a basket that isn't
    # theirs just by guessing an item id in the URL.

    item = get_object_or_404(basket.items, id=item_id)
    quantity = int(request.POST.get("quantity", 1))
    update_quantity(item, quantity)
    return redirect("basket:basket_detail")


@require_POST
def remove_basket_item(request, item_id):
    basket = get_or_create_basket(request)
    item = get_object_or_404(basket.items, id=item_id)
    item.delete()
    messages.success(request, "Item removed from your basket.")
    return redirect("basket:basket_detail")