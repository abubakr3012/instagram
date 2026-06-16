from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Profile


@admin.register(User)
class CustomUserAdmin(UserAdmin):

    list_display = (
        "id",
        "username",
        "email",
        "phone",
        "is_staff",
        "is_active",
    )

    search_fields = (
        "username",
        "email",
        "phone",
    )

    list_filter = (
        "is_staff",
        "is_active",
    )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "user",
        "follower_cnt",
        "following_cnt",
        "videos_cnt",
    )

    search_fields = (
        "user__username",
        "user__email",
    )

    list_filter = (
        "follower_cnt",
        "following_cnt",
    )