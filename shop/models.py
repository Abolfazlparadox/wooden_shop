from django.db import models
from django.conf import settings
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name="نام دسته")
    slug = models.SlugField(unique=True, verbose_name="اسلاگ")

    class Meta:
        verbose_name = "دسته بندی"
        verbose_name_plural = "دسته بندی ها"

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE, verbose_name="دسته بندی")
    title = models.CharField(max_length=255, verbose_name="عنوان")
    slug = models.SlugField(unique=True, verbose_name="اسلاگ")
    description = models.TextField(verbose_name="توضیحات")
    is_active = models.BooleanField(default=True, verbose_name="فعال")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")

    class Meta:
        verbose_name = "محصول"
        verbose_name_plural = "محصولات"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('shop:product_detail', kwargs={'slug': self.slug})


class ProductVariation(models.Model):
    product = models.ForeignKey(Product, related_name='variations', on_delete=models.CASCADE, verbose_name="محصول")
    sku = models.CharField(max_length=255, unique=True, verbose_name="شناسه محصول (SKU)")
    wood_type = models.CharField(max_length=255, default='Walnut', verbose_name="نوع چوب")
    dimensions = models.CharField(max_length=255, verbose_name="ابعاد")
    price = models.PositiveIntegerField(verbose_name="قیمت (تومان)")
    discount_price = models.PositiveIntegerField(null=True, blank=True, verbose_name="قیمت با تخفیف (تومان)")
    stock = models.PositiveIntegerField(default=0, verbose_name="موجودی انبار")
    preparation_days = models.PositiveIntegerField(default=0, verbose_name="روزهای آماده سازی")

    class Meta:
        verbose_name = "تنوع محصول"
        verbose_name_plural = "تنوع های محصول"

    def __str__(self):
        return f"{self.product.title} - {self.sku}"


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE, verbose_name="محصول")
    variation = models.ForeignKey(ProductVariation, related_name='images', on_delete=models.CASCADE, null=True, blank=True, verbose_name="تنوع")
    image = models.ImageField(upload_to='products/', verbose_name="تصویر")
    is_main = models.BooleanField(default=False, verbose_name="تصویر اصلی")

    class Meta:
        verbose_name = "تصویر محصول"
        verbose_name_plural = "تصاویر محصول"

    def __str__(self):
        return f"تصویر برای {self.product.title}"


class Review(models.Model):
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE, verbose_name="محصول")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='reviews', on_delete=models.CASCADE, verbose_name="کاربر")
    rating = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 6)], verbose_name="امتیاز")
    comment = models.TextField(verbose_name="متن نظر")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ثبت")

    class Meta:
        verbose_name = "نقد و بررسی"
        verbose_name_plural = "نقد و بررسی ها"

    def __str__(self):
        return f"نظر برای {self.product.title} توسط {self.user}"
