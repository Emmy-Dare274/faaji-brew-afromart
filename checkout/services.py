from .models import Order, OrderLineItem


def create_order_from_basket(user, basket, address_data):
    """The single place a basket turns into a real order. Copies
    each basket item's current price into price_at_purchase, then
    calls update_totals()"""
    order = Order.objects.create(user=user, **address_data)

    for item in basket.items.all():
        OrderLineItem.objects.create(
            order=order,
            product=item.product,
            variant=item.variant,
            quantity=item.quantity,
            price_at_purchase=item.unit_price,
        )

    order.update_totals()
    return order