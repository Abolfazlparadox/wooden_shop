from django.db import models
from django.conf import settings
from shop.models import ProductVariation


class Order(models.Model):
    SHIPPING_CHOICES = [
        ('tipax', 'تیپاکس (پس‌کرایه)'),
        ('barbari', 'باربری (پس‌کرایه)'),
    ]
    PAYMENT_CHOICES = [
        ('online', 'درگاه بانکی'),
        ('card', 'کارت به کارت'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    address = models.TextField()
    postal_code = models.CharField(max_length=20)
    shipping_method = models.CharField(max_length=20, choices=SHIPPING_CHOICES)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES)
    payment_receipt = models.ImageField(upload_to='receipts/', null=True, blank=True)
    total_price = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    tracking_code = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} by {self.full_name}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    variation = models.ForeignKey(ProductVariation, on_delete=models.SET_NULL, null=True)
    price = models.PositiveIntegerField()
    quantity = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.variation.sku if self.variation else 'N/A'}"


class CustomOrder(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('reviewed', 'Reviewed'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='custom_orders')
    customer_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    description = models.TextField()
    reference_image = models.ImageField(upload_to='custom_orders/', null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    proposed_price = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Custom Order by {self.customer_name} - {self.status}"
