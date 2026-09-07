from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from checkout.models import Order
from core.decorators import staff_required
from .forms import ReviewForm
from .models import Category, Product, Review


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
    current rating, other customers' approved reviews, and — for a
    signed-in shopper — their own review (if they've left one) or a
    form to write one (if they've bought the product). """

    product = get_object_or_404(
        Product.objects.with_rating(), slug=product_slug, is_active=True
    )
    variants = product.variants.all().order_by("variant_type", "value")

    approved_reviews = product.reviews.filter(is_approved=True).select_related("user")
    user_review = None
    has_purchased = False
    if request.user.is_authenticated:
        user_review = product.reviews.filter(user=request.user).first()
        has_purchased = Order.objects.filter(
            user=request.user, lineitems__product=product
        ).exists()
        approved_reviews = approved_reviews.exclude(user=request.user)

    context = {
        "product": product,
        "variants": variants,
        "approved_reviews": approved_reviews,
        "user_review": user_review,
        "has_purchased": has_purchased,
        "review_form": ReviewForm(instance=user_review) if user_review else ReviewForm(),
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


@login_required
@require_POST
def add_review(request, product_slug):

    """ Lets a signed-in customer leave one review per product, but
    only if they've actually bought it — reviews should reflect
    real experience with the product, not just an opinion formed
    from browsing the listing. The one-review-per-user-per-product
    rule is enforced in the database via Review's unique_together,
    this check just gives a friendlier message than a 500 error. """

    product = get_object_or_404(Product, slug=product_slug, is_active=True)

    has_purchased = Order.objects.filter(
        user=request.user, lineitems__product=product
    ).exists()
    if not has_purchased:
        messages.error(request, "You can only review products you've purchased.")
        return redirect("products:product_detail", product_slug=product_slug)

    if Review.objects.filter(product=product, user=request.user).exists():
        messages.error(request, "You've already reviewed this product — edit your review below instead.")
        return redirect("products:product_detail", product_slug=product_slug)

    form = ReviewForm(request.POST)
    if form.is_valid():
        review = form.save(commit=False)
        review.product = product
        review.user = request.user
        review.save()
        messages.success(request, "Thanks! Your review has been submitted and is awaiting approval.")
    else:
        messages.error(request, "Please fix the errors in your review and try again.")

    return redirect("products:product_detail", product_slug=product_slug)


@login_required
@require_POST
def edit_review(request, review_id):

    """ A user can only ever edit their own review — ownership is
    checked via the queryset filter below rather than trusted from
    the form, otherwise anyone could edit someone else's review by
    guessing an id in the URL. """

    review = get_object_or_404(Review, id=review_id, user=request.user)
    form = ReviewForm(request.POST, instance=review)
    if form.is_valid():
        review = form.save(commit=False)
        review.is_approved = False  # edited content needs re-approval
        review.save()
        messages.success(request, "Your review has been updated and is awaiting re-approval.")
    else:
        messages.error(request, "Please fix the errors in your review and try again.")
    return redirect("products:product_detail", product_slug=review.product.slug)


@login_required
@require_POST
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    product_slug = review.product.slug
    review.delete()
    messages.success(request, "Your review has been deleted.")
    return redirect("products:product_detail", product_slug=product_slug)


@staff_required
def review_moderation(request):

    """ Front-end moderation queue for staff, so approving reviews
    doesn't require Django admin access — same pattern staff product
    management (#29) will follow next. """

    pending_reviews = Review.objects.filter(is_approved=False).select_related("product", "user")
    return render(request, "products/review_moderation.html", {"pending_reviews": pending_reviews})


@staff_required
@require_POST
def approve_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    review.is_approved = True
    review.save()
    messages.success(request, f"Approved the review for {review.product.name}.")
    return redirect("products:review_moderation")


@staff_required
@require_POST
def reject_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    messages.success(request, f"Rejected and removed the review for {review.product.name}.")
    review.delete()
    return redirect("products:review_moderation")
