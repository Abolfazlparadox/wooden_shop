# blog/models.py

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Post(models.Model):
    STATUS_CHOICES = (
        ("draft", "پیش‌نویس"),
        ("published", "منتشر شده"),
    )

    title = models.CharField(max_length=200, verbose_name="عنوان پست")
    slug = models.SlugField(
        max_length=220, unique=True, allow_unicode=True, verbose_name="اسلاگ"
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="blog_posts",
        verbose_name="نویسنده",
    )
    content = models.TextField(verbose_name="محتوای پست")
    image = models.ImageField(upload_to="blog_images/", verbose_name="تصویر شاخص")
    tags = models.ManyToManyField(
        "shop.Tag",
        related_name="blog_posts",
        blank=True,
        verbose_name="برچسب‌ها",
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="draft", verbose_name="وضعیت"
    )

    class Meta:
        verbose_name = "پست وبلاگ"
        verbose_name_plural = "پست‌های وبلاگ"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("blog:post_detail", kwargs={"slug": self.slug})

    @property
    def reading_time(self):
        """Estimate reading time in minutes at ~250 words per minute."""
        word_count = len(self.content.split())
        return max(1, round(word_count / 250))


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="پست",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="blog_comments",
        verbose_name="کاربر",
    )
    # Used when commenter is a guest (not authenticated)
    name = models.CharField(max_length=100, blank=True, verbose_name="نام (مهمان)")
    body = models.TextField(verbose_name="متن نظر")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    is_active = models.BooleanField(default=True, verbose_name="فعال")

    class Meta:
        verbose_name = "نظر"
        verbose_name_plural = "نظرات"
        ordering = ["created_at"]

    def __str__(self):
        return f"نظر از {self.get_display_name()} برای «{self.post.title}»"

    def get_display_name(self):
        """Return the best available display name for this commenter."""
        if self.user:
            full_name = f"{self.user.first_name} {self.user.last_name}".strip()
            return full_name if full_name else self.user.phone_number
        return self.name or "مهمان ناشناس"
