from django.db import models


class Category(models.Model):
    """
    A product category (e.g. Bouquet)
    """

    class Meta:
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=200)
    display_name = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name
    
    def get_display_name(self):
        return self.display_name


class Product(models.Model):
    """
    Represent a product available in the store.
    """
    category = models.ForeignKey(
        Category, 
        null=True, 
        blank=True, 
        on_delete=models.SET_NULL)
    name = models.CharField(max_length=250)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    in_stock = models.BooleanField(default=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name
    