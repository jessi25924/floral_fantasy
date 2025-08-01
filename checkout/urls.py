from django.urls import path
from . import views
from .webhooks import webhook

urlpatterns = [
    path('', views.checkout, name='checkout'),
    path('checkout/success/', views.checkout_success, name='checkout_success'),
    path('wh/', webhook, name='webhook'),
]
