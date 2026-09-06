from .models import Basket


def basket_context(request):

    """ Makes the basket count and total available in every template
    automatically, the navbar included, without every single view
    having to fetch and pass it manually. Deliberately does NOT
    create a basket here, only looks one up if it already exists,
    so simply browsing the site never creates empty basket rows for
    every visitor. A basket only gets created the moment someone
    actually adds something."""
    
    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user).first()
    else:
        session_key = request.session.session_key
        basket = Basket.objects.filter(user=None, session_key=session_key).first() if session_key else None

    return {
        "basket_item_count": basket.item_count if basket else 0,
        "basket_total": basket.total if basket else 0,
    }