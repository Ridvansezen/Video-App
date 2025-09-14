from django.contrib import admin
from .models import Post, Comment, Like, SavedPost

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "content", "created_at")
    fields = ("user", "content", "image", "video", "like_count", "created_at", "updated_at")
    readonly_fields = ("created_at", "updated_at")
