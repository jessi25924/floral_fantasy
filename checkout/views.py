from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from .forms import OrderForm
from decimal import Decimal
from products.models import Product


def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.error(request, "Your cart is empty at the moment")
        return redirect(reverse('products'))
    
    order_form = OrderForm()
    
    cart_items = []
    subtotal = Decimal ('0.00')

    for pid_str, qty in cart.items():
        product = get_object_or_404(Product, pk=int(pid_str))
        line_total = product.price * qty
        subtotal += line_total
        cart_items.append({
            'product': product,
            'quantity': qty,
            'line_total': line_total,
        })

    delivery = Decimal('2.99') if subtotal > 0 else Decimal('0.00')
    grand_total = subtotal + delivery

    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'cart_items': cart_items,
        'subtotal': subtotal,
        'delivery': delivery,
        'grand_total': grand_total,
    }

    return render(request, template, context)