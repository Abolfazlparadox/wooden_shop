from django.contrib import admin

from .models import Category, Product, ProductImage, ProductVariation, Review, Tag


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
    list_display = ("product", "user", "rating", "is_approved", "parent", "created_at")
    list_filter = ("is_approved", "rating", "created_at")
    list_editable = ("is_approved",)
    search_fields = ("product__title", "user__phone_number", "comment")
    raw_id_fields = ("parent",)
    readonly_fields = ("created_at",)
    actions = ["approve_reviews", "reject_reviews"]

    @admin.action(description="✅ تایید نظرات انتخاب شده")
    def approve_reviews(self, request, queryset):
        count = queryset.update(is_approved=True)
        self.message_user(request, f"{count} نظر با موفقیت تایید شد.")

    @admin.action(description="❌ رد نظرات انتخاب شده")
    def reject_reviews(self, request, queryset):
        count = queryset.update(is_approved=False)
        self.message_user(request, f"{count} نظر رد شد.")
