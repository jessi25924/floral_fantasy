from django.shortcuts import render, redirect, get_object_or_404
from decimal import Decimal
from django.contrib import messages
from products.models import Product


def view_cart(request):
    """
    
    """
    return render(request, 'cart/cart.html')

def add_to_cart(request, product_id):
    """
    Add a quantity of the product to the cart, considering stock.
    """
    quantity = int(request.POST.get('quantity', 1))
    redirect_url = request.POST.get('redirect_url', '/')
    product = get_object_or_404(Product, pk=product_id)

    # If the product is marked out of stock, reject the add
    if not product.in_stock:
        messages.error(request, f'Sorry, "{product.name}" is currently out of stock.')
        return redirect(redirect_url)
    
    cart = request.session.get('cart', {})
    key = str(product_id)

    cart[key] = cart.get(key, 0) + quantity
    request.session['cart'] = cart

    messages.success(request, f'Added {quantity} × "{product.name}" to your cart.')
    return redirect(redirect_url)


def view_cart(request):
    """
    Display the contents of the user's shopping cart,
    including a flat delivery fee of 2.99.
    """
    cart = request.session.get('cart', {})
    cart_items = []
    subtotal = Decimal('0.00')

    for pid_str, qty in cart.items():
        product = get_object_or_404(Product, pk=int(pid_str))
        line_total = product.price * qty
        subtotal += line_total
        cart_items.append({
            'product':    product,
            'quantity':   qty,
            'line_total': line_total,
        })

    if subtotal > 0:
        delivery_charge = Decimal('2.99')
    else:
        delivery_charge = Decimal('0.00')
    
    grand_total = subtotal + delivery_charge

    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'delivery_charge': delivery_charge,
        'grand_total': grand_total,
    }
    return render(request, 'cart/cart.html', context)


def update_cart(request, product_id):
    """
    Update the quantity of a product in the cart.
    """
    qty = int(request.POST.get('quantity', 0))
    redirect_url = request.POST.get('redirect_url', '/')
    product = get_object_or_404(Product, pk=product_id)

    cart = request.session.get('cart', {})
    key = str(product_id)

    if qty <= 0:
        cart.pop(key, None)
        messages.info(request, f'Removed "{product.name}" from your cart.')
    else:
        if not product.in_stock:
            messages.error(request, f'Sorry, "{product.name}" is out of stock.')
        else:
            cart[key] = qty
            messages.success(request, f'Updated "{product.name}" quantity to {qty}.')
    
    request.session['cart'] = cart
    return redirect(redirect_url)


def remove_from_cart(request, product_id):
    """
    Remove a product entirely from the cart.
    """
    redirect_url = request.POST.get('redirect_url', '/')
    cart = request.session.get('cart', {})
    key = str(product_id)

    if key in cart:
        cart.pop(key)
        request.session['cart'] = cart
        messages.info(request, "Item removed from your cart.")
    return redirect(redirect_url)