from django.contrib import admin
from .models import Stories, Actualnost, Archive


@admin.register(Stories)
class StoriesAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'user',
        'file',
        'created_at',
        'expires_at',
        'likes_cnt',
        'views_cnt',
        'is_deleted',
    ]

    list_filter = [
        'is_deleted',
        'created_at',
    ]

    search_fields = [
        'user__username',
        'file',
    ]

    list_editable = [
        'is_deleted',
    ]

    ordering = ['-created_at']


@admin.register(Actualnost)
class ActualnostAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'user',
        'name',
        'get_stories',
        'is_deleted',
        'created_at'
    ]

    list_filter = [
        'is_deleted',
        'created_at',
    ]

    search_fields = [
        'name',
        'user__username',
        'stories__user__username'
    ]

    list_editable = [
        'is_deleted',
    ]

    ordering = ['-created_at']

    def get_stories(self, obj):
        return ", ".join(str(s.id) for s in obj.stories.all())

    get_stories.short_description = "Stories"


@admin.register(Archive)
class ArchiveAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'user',
        'stories',
        'archived_at'
    ]

    list_filter = [
        'archived_at'
    ]

    search_fields = [
        'user__username'
    ]

    ordering = ['-archived_at']