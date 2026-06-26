from django.db import models
from accounts.models import *
from django.db.models import Q

class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)  
    description = models.TextField(blank=True)    
    category = models.CharField(max_length=100, blank=True, null=True)
    subcategory = models.CharField(max_length=100, blank=True, null=True)
    sizes = models.CharField(max_length=200, blank=True, null=True)
    stock = models.IntegerField(default=0)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    is_popular = models.BooleanField(default=False)
    is_deactive = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='product_created')
    updated_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='product_updated')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'sa_product'
        
    def __str__(self):
        return self.name

    

class ProductImage(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name="product_image")
    image = models.ImageField(upload_to='products/')

    def __str__(self):
        return f"Image of {self.product.name}"



class Cart(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='cart')
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='cart_created')
    updated_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='cart_updated')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'sa_cart'
    
    @property
    def total_items(self):
        return self.items.filter(is_deleted=False).aggregate(total=models.Sum('quantity'))['total'] or 0
    
    @property
    def total_price(self):
        total = 0
        for item in self.items.filter(is_deleted=False):
            total += item.product.price * item.quantity
        return total
    
    def __str__(self):
        return f"Cart - {self.user.email}"


class CartItem(models.Model):

    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items'
    )

    product = models.ForeignKey(Product,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField(default=1)

    size = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    color = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    is_deleted = models.BooleanField(default=False)

    created_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        related_name='cartitem_created'
    )

    updated_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        related_name='cartitem_updated'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'sa_cart_item'

        constraints = [
            models.UniqueConstraint(
                fields=[
                    'cart',
                    'product',
                    'size',
                    'color'
                ],
                condition=Q(is_deleted=False),
                name='unique_active_cart_item'
            )
        ]

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
    

