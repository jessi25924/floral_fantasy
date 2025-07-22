from django.shortcuts import redirect, get_object_or_404
from products.models import Product


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


