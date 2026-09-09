from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.urls import reverse

from basket.services import get_or_create_basket, add_item
from checkout.models import Order
from products.models import Product
from .forms import ProfileForm
from .models import UserProfile, WishList, WishListItem


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

@login_required
def my_account(request):

    """ View and edit saved default delivery details. The profile
    is created on first visit if it doesn't exist yet, rather than
    requiring a signal or a data migration for existing users. """

    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Your details have been updated.")
            return redirect("profiles:my_account")
    else:
        form = ProfileForm(instance=profile)

    recent_orders = request.user.orders.all()[:3]
    return render(request, "profiles/my_account.html", {"form": form, "recent_orders": recent_orders})


@login_required
def order_history(request):
    orders = request.user.orders.all().prefetch_related("lineitems__product__images", "lineitems__variant")
    return render(request, "profiles/order_history.html", {"orders": orders})


@login_required
@require_POST
def reorder(request, order_number):

    """ Adds every item from a past order back into the current
    basket in one go. Skips anything that's since been discontinued
    or sold out rather than failing the whole reorder, and tells the
    customer exactly what was skipped and why. """

    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    basket = get_or_create_basket(request)

    added, skipped = 0, []
    for item in order.lineitems.all():
        if item.product.is_active and item.product.in_stock:
            add_item(basket, item.product, item.variant, item.quantity)
            added += 1
        else:
            skipped.append(item.product.name)

    if added:
        messages.success(
            request,
            f"Added {added} item{'s' if added != 1 else ''} from order {order.order_number} to your basket.",
        )
    if skipped:
        messages.warning(request, f"Couldn't add (no longer available): {', '.join(skipped)}.")

    return redirect("basket:basket_detail")