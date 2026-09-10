from .models import WishListItem


def wishlist_context(request):

    """Same pattern as the basket's context processor: makes the
    current user's saved product ids and count available on every
    page, so product cards know which hearts to fill without an
    extra query per card."""

    if not request.user.is_authenticated:
        return {"wishlist_item_ids": set(), "wishlist_count": 0}

    item_ids = set(
        WishListItem.objects.filter(wishlist__user=request.user)
        .values_list("product_id", flat=True)
    )
    return {"wishlist_item_ids": item_ids, "wishlist_count": len(item_ids)}
