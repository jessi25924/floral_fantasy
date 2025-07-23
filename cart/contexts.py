from django.shortcuts import get_object_or_404
from products.models import Product


def cart_contents(request):

    cart_items = []
    total = 0
    product_count = 0
    delivery = 0
    cart = request.session.get('cart', {})


    for item_id, quantity in cart.items():
        product = get_object_or_404(Product, pk=item_id)
        subtotal = quantity * product.price
        total += subtotal
        product_count += quantity
        cart_items.append({
            'item_id': item_id,
            'quantity': quantity,
            'product': product,
            'subtotal': subtotal,
        })

    grand_total = delivery + total

    context = {
        'cart_items': cart_items,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'grand_total': grand_total,
    }
    return context