from django.shortcuts import render, redirect, get_object_or_404
from products.models import Product


def view_cart(request):
    """
    
    """
    return render(request, 'cart/cart.html')

def add_to_cart(request, product_id):
    """
    Add a product to the user's cart session.
    """
    product = get_object_or_404(Product, pk=product_id)

    if not product.in_stock:
        # I could show a message here as well, will come back to this.
        return redirect('products:product_list')
    
    cart = request.session.get('cart', {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    request.session['cart'] = cart

    return redirect('product:product_list')


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
