from django.urls import path
from .views import ProductListView, ProductDetailView
from . import views


app_name = 'products'

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('add/', views.add_product, name='add_product'),
]