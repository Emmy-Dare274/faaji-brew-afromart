from .models import Basket, BasketItem


def get_or_create_basket(request):

    """ The single place that decides how to find or create the right
    basket for the current request, logged in or not. Every view
    that touches the basket calls this rather than writing its own
    lookup. """

    if request.user.is_authenticated:
        basket, _ = Basket.objects.get_or_create(user=request.user)
        return basket

    if not request.session.session_key:
        request.session.create()
    basket, _ = Basket.objects.get_or_create(
        user=None, session_key=request.session.session_key
    )
    return basket


def add_item(basket, product, variant=None, quantity=1):
    item, created = BasketItem.objects.get_or_create(
        basket=basket, product=product, variant=variant,
        defaults={"quantity": quantity},
    )
    if not created:
        item.quantity += quantity
        item.save()
    return item


def update_quantity(basket_item, quantity):
    if quantity <= 0:
        basket_item.delete()
        return None
    basket_item.quantity = quantity
    basket_item.save()
    return basket_item


def merge_guest_basket_into_user(request, user):

    """ Runs the moment someone logs in. Folds whatever they added
    while browsing anonymously into their real account basket, so
    nothing gets lost the moment they log in at checkout. """
    
    session_key = request.session.session_key
    if not session_key:
        return

    try:
        guest_basket = Basket.objects.get(user=None, session_key=session_key)
    except Basket.DoesNotExist:
        return

    user_basket, _ = Basket.objects.get_or_create(user=user)
    for guest_item in guest_basket.items.all():
        add_item(user_basket, guest_item.product, guest_item.variant, guest_item.quantity)
    guest_basket.delete()