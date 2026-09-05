from django.shortcuts import render

# Create your views here.

def home(request):
    """Renders the homepage. Currently static content only, since
    the products app doesn't have models yet. The featured products,
    category tiles, and testimonials sections get added here once
    there is real data to pull them from."""

    return render(request, "core/home.html")