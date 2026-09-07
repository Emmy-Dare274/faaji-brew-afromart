from django.shortcuts import render
from products.models import Category, Product

from django.http import HttpResponse
from django.template.loader import render_to_string


def home(request):

    """ Renders the homepage. Pulls categories and featured
    products now that the products app has models to query. """

    categories = Category.objects.active()
    featured_products = Product.objects.featured().with_rating()[:4]
    context = {
        "categories": categories,
        "featured_products": featured_products,
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
    the request (Heroku, or a future custom domain). """
    
    content = render_to_string(
        "core/robots.txt", {"domain": request.build_absolute_uri("/")[:-1]}
    )
    return HttpResponse(content, content_type="text/plain")