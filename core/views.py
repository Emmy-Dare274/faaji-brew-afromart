from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import render_to_string
from products.models import Category, Product, Review


def home(request):

    """ Renders the homepage. Pulls categories, featured products,
    and a handful of staff-featured, approved reviews for the
    testimonials carousel. """

    categories = Category.objects.active()
    featured_products = Product.objects.featured().with_rating()[:4]
    testimonials = Review.objects.filter(
        is_approved=True, is_featured=True
    ).select_related("user", "product")[:6]
    context = {
        "categories": categories,
        "featured_products": featured_products,
        "testimonials": testimonials,
    }
    return render(request, "core/home.html", context)


def our_story(request):
    return render(request, "core/our_story.html")


def terms_of_use(request):
    return render(request, "core/terms_of_use.html")


def privacy_policy(request):
    return render(request, "core/privacy_policy.html")


def robots_txt(request):

    """ Served as plain text rather than a static file so the
    Sitemap: line always points at whichever host actually served
    the request (Codespaces preview, Heroku, or a future custom
    domain) instead of a hardcoded URL that would go stale the
    moment the domain changes. """

    content = render_to_string(
        "core/robots.txt", {"domain": request.build_absolute_uri("/")[:-1]}
    )
    return HttpResponse(content, content_type="text/plain")