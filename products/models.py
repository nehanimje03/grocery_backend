from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='products/')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    old_price = models.DecimalField(max_digits=10, decimal_places=2)
    rating = models.FloatField(default=0)
    category = models.CharField(max_length=100)
    is_popular = models.BooleanField(default=False)

    def __str__(self):
        return self.name