from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product, ProductImage, ProductVariation, Review, Tag
from django.urls import reverse

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "parent", "is_sub")
    list_filter = ("is_sub",)
    prepopulated_fields = {"slug": ("name",)}


class ProductVariationInline(admin.TabularInline):
    model = ProductVariation
    extra = 1


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "is_active", "created_at")
    list_filter = ("category", "is_active")
    search_fields = ("title", "description", "tags__name")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [ProductVariationInline, ProductImageInline]
    filter_horizontal = ("tags",)


@admin.register(ProductVariation)
class ProductVariationAdmin(admin.ModelAdmin):
    list_display = (
        "sku",
        "product",
        "wood_type",
        "formatted_price",
        "formatted_discount_price",
        "stock",
    )
    list_filter = ("wood_type",)
    search_fields = ("sku", "product__title")

    def formatted_price(self, obj):
        return f"{obj.price:,} تومان" if obj.price is not None else "-"

    formatted_price.short_description = "قیمت"

    def formatted_discount_price(self, obj):
        return (
            f"{obj.discount_price:,} تومان" if obj.discount_price is not None else "-"
        )

    formatted_discount_price.short_description = "قیمت با تخفیف"


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ("product", "variation", "is_main")
    list_filter = ("is_main",)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'is_approved', 'created_at', 'reply_to_review')
    list_filter = ('is_approved', 'rating', 'created_at')
    search_fields = ('product__title', 'user__phone_number', 'comment')
    list_editable = ('is_approved',)
    autocomplete_fields = ('product', 'user', 'parent') # Makes dropdowns searchable

    def reply_to_review(self, obj):
        if obj.parent is None: # Only show for top-level comments
            url = reverse('admin:shop_review_add') + f'?parent={obj.id}'
            return format_html('<a href="{}">پاسخ به این نظر</a>', url)
        return "-"
    reply_to_review.short_description = 'پاسخ سریع'

    @admin.action(description="✅ تایید نظرات انتخاب شده")
    def approve_reviews(self, request, queryset):
        count = queryset.update(is_approved=True)
        self.message_user(request, f"{count} نظر با موفقیت تایید شد.")

    @admin.action(description="❌ رد نظرات انتخاب شده")
    def reject_reviews(self, request, queryset):
        count = queryset.update(is_approved=False)
        self.message_user(request, f"{count} نظر رد شد.")
