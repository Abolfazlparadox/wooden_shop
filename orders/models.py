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
        ('pending', 'در انتظار پرداخت'),
        ('processing', 'در حال پردازش'),
        ('shipped', 'ارسال شده'),
        ('cancelled', 'لغو شده'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders', verbose_name="کاربر")
    full_name = models.CharField(max_length=255, verbose_name="نام کامل تحویل گیرنده")
    phone_number = models.CharField(max_length=20, verbose_name="شماره تلفن")
    address = models.TextField(verbose_name="آدرس کامل")
    postal_code = models.CharField(max_length=20, verbose_name="کد پستی")
    shipping_method = models.CharField(max_length=20, choices=SHIPPING_CHOICES, verbose_name="روش ارسال")
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES, verbose_name="روش پرداخت")
    payment_receipt = models.ImageField(upload_to='receipts/', null=True, blank=True, verbose_name="رسید پرداخت")
    total_price = models.PositiveIntegerField(verbose_name="مبلغ کل (تومان)")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="وضعیت سفارش")
    tracking_code = models.CharField(max_length=50, null=True, blank=True, verbose_name="کد رهگیری")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ثبت")

    class Meta:
        verbose_name = "سفارش"
        verbose_name_plural = "سفارشات"
        ordering = ['-created_at']

    def __str__(self):
        return f"سفارش {self.id} توسط {self.full_name}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, verbose_name="سفارش")
    variation = models.ForeignKey(ProductVariation, on_delete=models.SET_NULL, null=True, verbose_name="تنوع محصول")
    price = models.PositiveIntegerField(verbose_name="قیمت در زمان خرید")
    quantity = models.PositiveSmallIntegerField(default=1, verbose_name="تعداد")

    class Meta:
        verbose_name = "آیتم سفارش"
        verbose_name_plural = "آیتم های سفارش"

    def __str__(self):
        return f"{self.quantity} عدد از {self.variation.sku if self.variation else 'N/A'}"


class CustomOrder(models.Model):
    STATUS_CHOICES = [
        ('pending', 'در انتظار بررسی'),
        ('reviewed', 'بررسی شده'),
        ('accepted', 'پذیرفته شده'),
        ('rejected', 'رد شده'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='custom_orders', verbose_name="کاربر")
    customer_name = models.CharField(max_length=255, verbose_name="نام مشتری")
    phone_number = models.CharField(max_length=20, verbose_name="شماره تلفن")
    description = models.TextField(verbose_name="توضیحات سفارش")
    reference_image = models.ImageField(upload_to='custom_orders/', null=True, blank=True, verbose_name="تصویر مرجع")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="وضعیت")
    proposed_price = models.PositiveIntegerField(null=True, blank=True, verbose_name="قیمت پیشنهادی (تومان)")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ثبت")

    class Meta:
        verbose_name = "سفارش اختصاصی"
        verbose_name_plural = "سفارشات اختصاصی"
        ordering = ['-created_at']

    def __str__(self):
        return f"سفارش اختصاصی توسط {self.customer_name} - {self.status}"
