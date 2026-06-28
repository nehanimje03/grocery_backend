from django.utils import timezone
from decimal import Decimal
import random
import time
from django.db import models
from accounts.models import *
from products.models import *



class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('PROCESSING', 'Processing'),
        ('PACKED', 'Packed'),
        ('SHIPPED', 'Shipped'),
        ('OUT_FOR_DELIVERY', 'Out for Delivery'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED', 'Cancelled'),
        ('RETURN_REQUESTED', 'Return Requested'),
        ('RETURN_APPROVED', 'Return Approved'),
        ('RETURNED', 'Returned'),
        ('REFUNDED', 'Refunded'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PAID', 'Paid'),
        ('FAILED', 'Failed'),
        ('REFUNDED', 'Refunded'),
        ('UNPAID', 'Unpaid'),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('COD', 'Cash On Delivery'),
        ('STRIPE', 'Stripe'),
    ]

    order_id = models.CharField(max_length=30, unique=True, editable=False, db_index=True)
    tracking_number = models.CharField(max_length=100, blank=True, null=True, db_index=True)
    invoice_number = models.CharField(max_length=100, blank=True, null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='orders')
    shipping_name = models.CharField(max_length=255)
    shipping_email = models.EmailField()
    shipping_phone = models.CharField(max_length=20)
    shipping_alternate_phone = models.CharField(max_length=20, blank=True, null=True)
    shipping_address_line1 = models.TextField()
    shipping_address_line2 = models.TextField(blank=True, null=True)
    shipping_landmark = models.CharField(max_length=255, blank=True, null=True)
    shipping_city = models.CharField(max_length=100)
    shipping_state = models.CharField(max_length=100)
    shipping_pincode = models.CharField(max_length=20)
    shipping_country = models.CharField(max_length=100, default='India')
    same_as_shipping = models.BooleanField(default=True)
    billing_name = models.CharField(max_length=255, blank=True, null=True)
    billing_address = models.TextField(blank=True, null=True)
    billing_city = models.CharField(max_length=100, blank=True, null=True)
    billing_state = models.CharField(max_length=100, blank=True, null=True)
    billing_pincode = models.CharField(max_length=20, blank=True, null=True)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    discount_amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    shipping_charge = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    tax_amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    payment_status = models.CharField(max_length=20,choices=PAYMENT_STATUS_CHOICES,default='PENDING',db_index=True)
    payment_id = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    stripe_session_id = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    payment_response = models.JSONField(blank=True, null=True)
    payment_failure_reason = models.TextField(blank=True, null=True)
    payment_completed_at = models.DateTimeField(blank=True, null=True)
    payment_expiry = models.DateTimeField(blank=True, null=True)
    is_payment_expired = models.BooleanField(default=False)
    status = models.CharField(max_length=30,choices=ORDER_STATUS_CHOICES,default='PENDING',db_index=True)
    order_note = models.TextField(blank=True, null=True)
    admin_notes = models.TextField(blank=True, null=True)
    cancel_reason = models.TextField(blank=True, null=True)
    cancelled_by = models.ForeignKey(CustomUser,on_delete=models.SET_NULL,null=True,blank=True,related_name='cancelled_orders')
    estimated_delivery_date = models.DateField(blank=True, null=True)
    delivered_to = models.CharField(max_length=255, blank=True, null=True)
    order_date = models.DateTimeField(auto_now_add=True, db_index=True)
    confirmed_at = models.DateTimeField(blank=True, null=True)
    processed_at = models.DateTimeField(blank=True, null=True)
    packed_at = models.DateTimeField(blank=True, null=True)
    shipped_at = models.DateTimeField(blank=True, null=True)
    delivered_at = models.DateTimeField(blank=True, null=True)
    cancelled_at = models.DateTimeField(blank=True, null=True)
    returned_at = models.DateTimeField(blank=True, null=True)
    refunded_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(CustomUser,on_delete=models.SET_NULL,null=True,related_name='orders_created')
    updated_by = models.ForeignKey(CustomUser,on_delete=models.SET_NULL,null=True,blank=True,related_name='orders_updated')

    class Meta:
        db_table = 'sa_order'
        ordering = ['-order_date']

        indexes = [
            models.Index(fields=['order_id']),
            models.Index(fields=['user']),
            models.Index(fields=['status']),
            models.Index(fields=['payment_status']),
            models.Index(fields=['payment_method']),
            models.Index(fields=['order_date']),
            models.Index(fields=['tracking_number']),
            models.Index(fields=['payment_id']),
        ]

    def save(self, *args, **kwargs):
        if not self.order_id:
            timestamp = int(time.time())
            random_num = random.randint(1000, 9999)
            self.order_id = f"FRV{timestamp}{random_num}"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order #{self.order_id} - {self.user.email}"

    @property
    def total_items(self):
        return self.items.aggregate(total=models.Sum('quantity'))['total'] or 0

    @property
    def order_status_display(self):
        return dict(self.ORDER_STATUS_CHOICES).get(self.status, self.status)

    @property
    def can_cancel(self):
        return self.status in ['PENDING', 'CONFIRMED', 'PROCESSING']

    @property
    def can_return(self):
        if self.status == 'DELIVERED' and self.delivered_at:
            days_since_delivery = (timezone.now() - self.delivered_at).days
            return days_since_delivery <= 7

        return False

    @property
    def is_expired(self):
        if self.payment_expiry and timezone.now() > self.payment_expiry:
            return True

        return False

    def mark_payment_failed(self, reason=None):
        self.payment_status = 'FAILED'
        self.payment_failure_reason = reason
        self.save()

    def mark_payment_success(self, payment_id=None):
        self.payment_status = 'PAID'
        self.payment_id = payment_id
        self.payment_completed_at = timezone.now()
        self.status = 'CONFIRMED'
        self.confirmed_at = timezone.now()
        self.save()

    def cancel_order(self, reason=None, user=None):
        self.status = 'CANCELLED'
        self.cancel_reason = reason
        self.cancelled_by = user
        self.cancelled_at = timezone.now()
        self.save()


class OrderItem(models.Model):    
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255)
    product_image = models.CharField(max_length=500, blank=True, null=True)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    original_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount_percentage = models.IntegerField(default=0)
    quantity = models.IntegerField()
    size = models.CharField(max_length=20, blank=True, null=True)
    color = models.CharField(max_length=50, blank=True, null=True)
    is_return_requested = models.BooleanField(default=False)
    return_reason = models.TextField(blank=True, null=True)
    return_status = models.CharField(max_length=50, blank=True, null=True)
    return_requested_at = models.DateTimeField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'sa_order_item'
    
    @property
    def subtotal(self):
        return self.product_price * self.quantity
    
    def __str__(self):
        return f"{self.quantity} x {self.product_name}"


class OrderTracking(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='tracking_history')
    status = models.CharField(max_length=50)
    location = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'sa_order_tracking'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.order.order_id} - {self.status} - {self.created_at}"


class Notify_Admin(models.Model):

    order = models.ForeignKey(
        "Order",
        on_delete=models.CASCADE,
        related_name="admin_notifications"
    )

    title = models.CharField(
        max_length=255
    )

    message = models.TextField()

    is_read = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        db_table = "notify_admin"
        ordering = ["-id"]

    def __str__(self):
        return f"{self.title} - {self.order.order_id}"