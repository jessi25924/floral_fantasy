from django.contrib import admin
from django.urls import path
from .views import contact_submit
from . import views

urlpatterns = [
    path('', views.index, name='landing'),
    path("contact/submit/", contact_submit, name="contact_submit"),
]
