from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from .forms import OrderForm
from decimal import Decimal
from products.models import Product

from django.conf import settings
from .models import Order, OrderLineItem
from profiles.forms import UserProfileForm
from profiles.models import UserProfile
from cart.contexts import cart_contents

import stripe
import json


DISCOUNT_CODE = {
    'SUMMER10': Decimal('0.10'),
}


@require_POST
def cache_checkout_data(request):
    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'cart': json.dumps(request.session.get('cart', {})),
            'save_info': request.POST.get('save_info'),
            'username': request.user,
        })
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, 'Sorry, your payment cannot be \
            processed right now. Please try again later.')
        return HttpResponse(content=e, status=400)


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
                order = order_form.save(commit=False)
                
                order.discount_code = discount_code
                order.discount_amount = discount_amount

                order.delivery_cost = delivery
                order.save()

                for item in cart_items:
                    OrderLineItem.objects.create(
                        order=order,
                        product=item['product'],
                        quantity=item['quantity'],
                        lineitem_total=item['line_total'],
                    )
                
                request.session['cart'] = {}
                messages.success(request, "Payment successful! Your order is confirmed.")
                return redirect('checkout_success', order_number=order.order_number)

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


def checkout_success(request, order_number):
    """
    Handle successful checkouts
    """
    save_info = request.session.get('save_info')
    order = get_object_or_404(Order, order_number=order_number)

    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user=request.user)
        # Attach the user's profile to the order
        order.user_profile = profile
        order.save()

        # Save the user's info
        if save_info:
            profile_data = {
                'default_phone_number': order.phone_number,
                'default_country': order.country,
                'default_postcode': order.postcode,
                'default_town_or_city': order.town_or_city,
                'default_street_address1': order.street_address1,
                'default_street_address2': order.street_address2,
                'default_county': order.county,
            }
            user_profile_form = UserProfileForm(profile_data, instance=profile)
            if user_profile_form.is_valid():
                user_profile_form.save()

    messages.success(request, f'Order successfully processed! \
        Your order number is {order_number}. A confirmation \
        email will be sent to {order.email}.')

    if 'cart' in request.session:
        del request.session['cart']

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
    }

    return render(request, template, context)