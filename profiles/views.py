from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.urls import reverse

from products.models import Product
from .models import WishList, WishListItem


@login_required
def wishlist_detail(request):
    wishlist, _ = WishList.objects.get_or_create(user=request.user)
    products = Product.objects.filter(
        id__in=wishlist.items.values_list("product_id", flat=True), is_active=True
    ).with_rating()
    return render(request, "profiles/wishlist_detail.html", {"products": products})



@require_POST
def toggle_wishlist(request, product_slug):
    is_ajax = request.headers.get("x-requested-with") == "XMLHttpRequest"

    if not request.user.is_authenticated:
        return_to = request.POST.get("next") or reverse("core:home")
        login_url = f"{reverse('account_login')}?next={return_to}"
        if is_ajax:
            return JsonResponse({"login_required": True, "login_url": login_url}, status=401)
        messages.info(request, "Please log in to save items to your favourites.")
        return redirect(login_url)

    product = get_object_or_404(Product, slug=product_slug, is_active=True)
    wishlist, _ = WishList.objects.get_or_create(user=request.user)
    item, created = WishListItem.objects.get_or_create(wishlist=wishlist, product=product)

    if not created:
        item.delete()
        wishlisted = False
    else:
        wishlisted = True

    if is_ajax:
        return JsonResponse({"wishlisted": wishlisted, "count": wishlist.items.count()})

    messages.success(
        request,
        f"Added {product.name} to your favourites." if wishlisted else f"Removed {product.name} from your favourites.",
    )
    return redirect(request.POST.get("next") or "core:home")