from django.contrib import admin
from .models import Post

@admin.register(Post)
class Post(admin.ModelAdmin):
    list_display=(
    "id",
    "user",
    "photo",
    "music",
    "created_at",
    )
    search_fields=(
        "user__username",
    )
    list_filter=(
        "created_at",
    )
