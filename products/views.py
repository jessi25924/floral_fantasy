from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Product


class ProductListView(ListView):
    """
    Display a paginated list of all products.
    """
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'
    paginate_by = 8


class ProductDetailView(DetailView):
    """
    SHow full details for a singel product.
    """
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'