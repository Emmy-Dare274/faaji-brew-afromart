from .models import Category


def nav_categories(request):

    """ Makes the live category list available in the navbar on every
    page."""

    return {"nav_categories": Category.objects.active()}