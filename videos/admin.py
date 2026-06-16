from django.contrib import admin
from .models import Videos, Reposts, SavedVideos


@admin.register(Videos)
class VideosAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'title', 'likes_cnt', 
                    'views_cnt', 'comment_cnt', 'created_at', 'is_deleted']
    list_filter = ['is_deleted', 'created_at']
    search_fields = ['title', 'user__username']
    readonly_fields = ['likes_cnt', 'views_cnt', 'comment_cnt', 'created_at']
    list_editable = ['is_deleted']


@admin.register(Reposts)
class RepostsAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'video', 'reposted_at', 'is_deleted']
    list_filter = ['is_deleted']
    search_fields = ['user__username', 'video__title']
    list_editable = ['is_deleted']


@admin.register(SavedVideos)
class SavedVideosAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'video', 'saved_at', 'is_deleted']
    list_filter = ['is_deleted']
    search_fields = ['user__username', 'video__title']
    list_editable = ['is_deleted']