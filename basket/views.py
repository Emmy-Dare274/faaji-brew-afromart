from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.http import JsonResponse

from products.models import Product, ProductVariant
from .services import get_or_create_basket, add_item, update_quantity


def _safe_quantity(raw_value, default=1):
    
    """Never lets a malformed quantity value reach further into the
    view. Anything that isn't a positive whole number quietly falls
    back to the default instead of crashing the request."""
    try:
        value = int(raw_value)
    except (TypeError, ValueError):
        return default
    return value if value > 0 else default


def basket_detail(request):
    basket = get_or_create_basket(request)
    return render(request, "basket/basket_detail.html", {"basket": basket})


@require_POST
def add_to_basket(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug, is_active=True)
    quantity = _safe_quantity(request.POST.get("quantity"))
    is_ajax = request.headers.get("x-requested-with") == "XMLHttpRequest"

    variant_id = request.POST.get("variant_id")
    variant = None
    if variant_id and variant_id.isdigit():
        variant = get_object_or_404(ProductVariant, id=variant_id, product=product)

    available = variant.stock_quantity if variant else product.stock_quantity
    if available < quantity:
        error_msg = f"Sorry, only {available} of {product.name} left in stock."
        if is_ajax:
            return JsonResponse({"success": False, "error": error_msg}, status=400)
        messages.error(request, error_msg)
        return redirect("products:product_detail", product_slug=product.slug)

    basket = get_or_create_basket(request)
    add_item(basket, product, variant, quantity)

    if is_ajax:
        items_data = []
        for basket_item in basket.items.all():
            item_image = basket_item.product.primary_image
            items_data.append({
                "product_name": basket_item.product.name,
                "product_image": item_image.image.url if item_image else "",
                "quantity": basket_item.quantity,
                "variant": str(basket_item.variant) if basket_item.variant else "",
                "line_total": f"{basket_item.line_total:.2f}",
            })
        return JsonResponse({
            "success": True,
            "added_product_name": product.name,
            "items": items_data,
            "basket_total": f"{basket.total:.2f}",
            "basket_item_count": basket.item_count,
            "amount_to_free_delivery": f"{basket.amount_to_free_delivery:.2f}",
            "qualifies_for_free_delivery": basket.qualifies_for_free_delivery,
        })
    
    messages.success(request, f"Added {product.name} to your basket.")
    return redirect("basket:basket_detail")


@require_POST
def update_basket_item(request, item_id):
    basket = get_or_create_basket(request)
    # Looking the item up through basket.items, not BasketItem
    # directly, stops someone editing a basket that isn't theirs
    # just by guessing an item id in the URL.
    item = get_object_or_404(basket.items, id=item_id)
    quantity = _safe_quantity(request.POST.get("quantity"))
    update_quantity(item, quantity)
    return redirect("basket:basket_detail")


@require_POST
def remove_basket_item(request, item_id):
    basket = get_or_create_basket(request)
    item = get_object_or_404(basket.items, id=item_id)
    item.delete()
    messages.success(request, "Item removed from your basket.")
    return redirect("basket:basket_detail")