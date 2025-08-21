from django.shortcuts import redirect, reverse, render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.db.models import Q
from django.db.models.functions import Lower
from django.contrib import messages

from .models import Product
from .forms import ProductForm


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


def add_product(request):
    """ Add a product to the store """
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully added product!')
            return redirect(reverse( 'products:add_product'))
        else:
            messages.error(request, 'Failed to add product. Please ensure the form is valid.')
    else:
        form = ProductForm()
        
    template = 'products/add_product.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


def edit_product(request, product_id):
    """ Edit a product in the store """
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated product!')
            return redirect(reverse('products:product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to update product. Please ensure the form is valid.')
    else:
        form = ProductForm(instance=product)
        messages.info(request, f'You are editing {product.name}')

    template = 'products/edit_product.html'
    context = {
        'form': form,
        'product': product,
    }

    return render(request, template, context)