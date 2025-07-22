from django.contrib import admin
from .models import Product, Category


# Inspired by code from the CI walkthrough lesson - adapted for this project.
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'category',
        'description',
        'price',
        'in_stock',
        'image',
    )

    ordering = ('category',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'display_name',
    )


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
