# blog/models.py

from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'پیش‌نویس'),
        ('published', 'منتشر شده'),
    )

    title = models.CharField(max_length=200, verbose_name="عنوان پست")
    slug = models.SlugField(max_length=220, unique=True, allow_unicode=True, verbose_name="اسلاگ")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='blog_posts',
                               verbose_name="نویسنده")
    content = models.TextField(verbose_name="محتوای پست")
    image = models.ImageField(upload_to='blog_images/', verbose_name="تصویر شاخص")
    tags = models.ManyToManyField('shop.Tag', related_name='blog_posts', blank=True, verbose_name='برچسب‌ها')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft', verbose_name="وضعیت")

    class Meta:
        verbose_name = "پست وبلاگ"
        verbose_name_plural = "پست‌های وبلاگ"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'slug': self.slug})