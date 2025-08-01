from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from .forms import OrderForm
from decimal import Decimal
from products.models import Product

from django.conf import settings
import stripe


DISCOUNT_CODE = {
    'SUMMER10': Decimal('0.10'),
}


def checkout(request):
    """
    Display the checkout page, calculate subtotal, delivery, 
    optional discount, and grand total. 
    """
    cart = request.session.get('cart', {})
    if not cart:
        messages.error(request, "Your cart is empty at the moment")
        return redirect(reverse('products'))

    # Build cart items & subtotal
    cart_items = []
    subtotal = Decimal('0.00')
    for pid_str, qty in cart.items():
        product = get_object_or_404(Product, pk=int(pid_str))
        line_total = product.price * qty
        subtotal += line_total
        cart_items.append({
            'product': product,
            'quantity': qty,
            'line_total': line_total,
        })

    # Compute delivery
    delivery = Decimal('2.99') if subtotal > 0 else Decimal('0.00')

    # Handle discount code
    discount_code = ''
    discount_amount = Decimal('0.00')
    if request.method == 'POST':
        code_input = request.POST.get('discount_code', '').strip().upper()
        discount_rate = DISCOUNT_CODE.get(code_input)
        if discount_rate:
            discount_code = code_input
            discount_amount = (subtotal * discount_rate).quantize(Decimal('0.01'))
            messages.success(request, f"Discount code '{code_input}' applied!")
        elif code_input:
            messages.error(request, f"Discount code '{code_input}' is invalid.")

    # Grand total after discount
    grand_total = subtotal - discount_amount + delivery

    # Stripe setup
    stripe.api_key = settings.STRIPE_SECRET_KEY
    client_secret = None
    stripe_public_key = settings.STRIPE_PUBLIC_KEY

    # Always have an unbound form ready for rendering
    order_form = OrderForm()

    # Final step: payment confirmation
    if request.method == 'POST' and 'payment_intent_id' in request.POST:
        order_form = OrderForm(request.POST)
        if order_form.is_valid():
            pi = stripe.PaymentIntent.retrieve(request.POST['payment_intent_id'])
            if pi.status == 'succeeded':
                messages.success(request, "Payment successful! Your order is confirmed.")
                # TODO: Save order, clear cart, etc.
                return render(request, 'checkout/checkout.html', {
                    'payment_success': True,
                    'stripe_public_key': stripe_public_key,
                    'order_form': order_form,  # Still needed in template
                })

    # Only create PaymentIntent if it's not the final post-back
    if not (request.method == 'POST' and 'payment_intent_id' in request.POST):
        intent = stripe.PaymentIntent.create(
            amount=int(grand_total * 100),
            currency='usd',
            metadata={
                'discount_code': discount_code or '',
            }
        )
        client_secret = intent.client_secret

    return render(request, 'checkout/checkout.html', {
        'order_form':        order_form,
        'cart_items':        cart_items,
        'subtotal':          subtotal,
        'delivery':          delivery,
        'discount_code':     discount_code,
        'discount_amount':   discount_amount,
        'grand_total':       grand_total,
        'stripe_public_key': stripe_public_key,
        'client_secret':     client_secret,
    })
    