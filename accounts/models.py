from django.db import models
from django.conf import settings
from django.utils import timezone
from .managers import CustomUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

class CustomUser(AbstractBaseUser, PermissionsMixin):
    phone_number = models.CharField(max_length=11, unique=True, verbose_name="شماره تلفن")
    first_name = models.CharField(max_length=255, blank=True, verbose_name="نام")
    last_name = models.CharField(max_length=255, blank=True, verbose_name="نام خانوادگی")
    is_active = models.BooleanField(default=True, verbose_name="فعال")
    is_staff = models.BooleanField(default=False, verbose_name="کارمند")
    is_phone_verified = models.BooleanField(default=False, verbose_name="تلفن تایید شده")
    date_joined = models.DateTimeField(default=timezone.now, verbose_name="تاریخ عضویت")

    objects = CustomUserManager()

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "کاربر"
        verbose_name_plural = "کاربران"

    def __str__(self):
        return self.phone_number

class OTP(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='otps', verbose_name="کاربر")
    code = models.CharField(max_length=6, verbose_name="کد تایید")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    is_used = models.BooleanField(default=False, verbose_name="استفاده شده")

    class Meta:
        verbose_name = "کد تایید"
        verbose_name_plural = "کدهای تایید"

    def __str__(self):
        return f"OTP for {self.user.phone_number}"

class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='addresses', verbose_name="کاربر")
    full_name = models.CharField(max_length=255, verbose_name="نام کامل تحویل گیرنده")
    state = models.CharField(max_length=100, verbose_name="استان")
    city = models.CharField(max_length=100, verbose_name="شهر")
    postal_code = models.CharField(max_length=20, verbose_name="کد پستی")
    full_address = models.TextField(verbose_name="آدرس کامل")
    phone_number = models.CharField(max_length=20, verbose_name="شماره تماس اضطراری")
    is_default = models.BooleanField(default=False, verbose_name="آدرس پیش فرض")

    class Meta:
        verbose_name = "آدرس"
        verbose_name_plural = "آدرس‌ها"

    def __str__(self):
        return f"آدرس برای {self.user.phone_number} در {self.city}"

    def save(self, *args, **kwargs):
        # If this address is being set as default, unset all others for this user
        if self.is_default:
            Address.objects.filter(user=self.user, is_default=True).update(is_default=False)
        super().save(*args, **kwargs)
