from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMessage
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.template.loader import render_to_string
from products.models import Category, Product, Review
from .forms import ContactForm


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

def delivery_returns(request):
    return render(request, "core/delivery_returns.html")


def faq(request):
    return render(request, "core/faq.html")


def contact_us(request):

    """ A real contact form, it sends an actual email through the same 
    SMTP backend that already sends order confirmations and newsletter 
    emails, straight to the business inbox. """

    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            email = EmailMessage(
                subject=f"AfroMart contact form message from {form.cleaned_data['name']}",
                body=(
                    f"From: {form.cleaned_data['name']} <{form.cleaned_data['email']}>\n\n"
                    f"{form.cleaned_data['message']}"
                ),
                to=[settings.DEFAULT_FROM_EMAIL],
                reply_to=[form.cleaned_data["email"]],
            )
            email.send()
            messages.success(request, "Thanks for reaching out — we'll get back to you soon.")
            return redirect("core:contact_us")
    else:
        form = ContactForm()

    return render(request, "core/contact_us.html", {"form": form})