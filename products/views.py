from django.shortcuts import redirect, reverse
from django.views.generic import ListView, DetailView
from django.db.models import Q
from django.db.models.functions import Lower
from django.contrib import messages

from .models import Product, Category


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
            return redirect(reverse('products'))
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        qs = super().get_queryset()
        params = self.request.GET

        # ——— Sorting ———
        sort_field = params.get('sort')
        direction = params.get('direction')
        if sort_field:
            # Case‑insensitive sort on name
            if sort_field == 'name':
                qs = qs.annotate(lower_name=Lower('name'))
                sort_field = 'lower_name'
            if direction == 'desc':
                sort_field = f'-{sort_field}'
            qs = qs.order_by(sort_field)

        # ——— Category filter ———
        if 'category' in params:
            names = params['category'].split(',')
            qs = qs.filter(category__name__in=names)

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

        # echo current search term
        ctx['search_term'] = params.get('q', '')

        # build current category queryset for template badges/links
        if 'category' in params:
            names = params['category'].split(',')
            ctx['current_categories'] = Category.objects.filter(name__in=names)
        else:
            ctx['current_categories'] = []

        # let template know current sort & direction
        sort = params.get('sort', '')
        direction = params.get('direction', '')
        ctx['current_sorting'] = f"{sort}.{direction}" if sort else ''

        return ctx


class ProductDetailView(DetailView):
    """
    SHow full details for a singel product.
    """
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'