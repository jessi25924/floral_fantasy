from django.shortcuts import render, redirect, get_object_or_404
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
    
    cart = request.session.get('bag', {})
    cart[product_id] = cart.get(product_id, 0) + quantity
    request.session['cart'] = cart

    messages.success(request, f'Added {quantity} x "{product.name}" to your cart.')
    print(request.session['cart'])
    return redirect(redirect_url)


def cart_detail(request):
    """
    Display the current session‐based shopping cart.
    """
    cart = request.session.get('cart', {})
    items = []
    total_price = 0

    for pid, data in cart.items():
        product = get_object_or_404(Product, pk=int(pid))
        qty = data.get('quantity', 0)
        subtotal = product.price * qty
        items.append({
            'product': product,
            'quantity': qty,
            'subtotal': subtotal,
        })
        total_price += subtotal

    return render(request, 'cart/cart_detail.html', {
        'items': items,
        'total_price': total_price,
    })
