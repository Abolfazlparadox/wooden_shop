# blog/admin.py

from django.contrib import admin

from .models import Comment, Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "status", "created_at", "updated_at")
    list_filter = ("status", "author", "created_at")
    search_fields = ("title", "content", "tags__name")
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("tags",)
    date_hierarchy = "created_at"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("post", "get_display_name", "is_active", "created_at")
    list_filter = ("is_active", "created_at")
    search_fields = ("name", "body", "post__title", "user__phone_number")
    list_editable = ("is_active",)
    raw_id_fields = ("post", "user")
    readonly_fields = ("created_at",)

    @admin.display(description="نام")
    def get_display_name(self, obj):
        return obj.get_display_name()
