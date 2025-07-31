from django.shortcuts import redirect, reverse
from django.views.generic import ListView, DetailView
from django.db.models import Q
from django.db.models.functions import Lower
from django.contrib import messages

from .models import Product


class ProductListView(ListView):
    """
    Display a paginated list of all products.
    """
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'
    paginate_by = 8


    def get(self, request, *args, **kwargs):
        # Prevent empty search submissions
        if 'q' in request.GET and not request.GET['q'].strip():
            messages.error(request, "Please enter a search term.")
            return redirect(reverse('products:product_list'))
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        qs = super().get_queryset()
        params = self.request.GET

        # ——— Sorting ———
        sort_field = params.get('sort')
        direction = params.get('direction', 'asc')
        if sort_field:
            # Case‑insensitive sort on name
            if sort_field == 'name':
                qs = qs.annotate(sort_name=Lower('name'))
                real_field = 'sort_name'
            elif sort_field == 'category':
                qs = qs.annotate(sort_cat=Lower('category__name'))
                real_field = 'sort_cat'
            else:
                real_field = sort_field

            if direction == 'desc':
                real_field = '-' + real_field
            qs = qs.order_by(real_field)

        # ——— Search ———
        if 'q' in params:
            term = params['q']
            qs = qs.filter(
                Q(name__icontains=term) |
                Q(description__icontains=term)
            )

        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        params = self.request.GET

       
        ctx['search_term'] = params.get('q', '')
        ctx['sort_field'] = params.get('sort', '')
        ctx['direction']  = params.get('direction', '')

        ctx['discount_code']= 'SUMMER10'

        return ctx


class ProductDetailView(DetailView):
    """
    SHow full details for a singel product.
    """
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'