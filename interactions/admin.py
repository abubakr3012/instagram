from django.contrib import admin
from .models import Comment, Like


class ReplyInline(admin.TabularInline):
    model = Comment
    fk_name = "parent_comment"
    fields = ["user", "comment_text", "is_deleted", "created_at"]
    readonly_fields = ["created_at"]
    extra = 0
    show_change_link = True


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = [
        "id", "user", "video", "short_text",
        "is_reply", "likes_count", "reply_count", "is_deleted", "created_at",
    ]
    list_filter = ["is_deleted", "created_at", "video"]
    search_fields = ["user__username", "comment_text", "video__title"]
    readonly_fields = ["created_at"]
    list_editable = ["is_deleted"]
    inlines = [ReplyInline]
    list_per_page = 30

    @admin.display(description="Текст")
    def short_text(self, obj):
        return obj.comment_text[:60]

    @admin.display(description="Ответ?", boolean=True)
    def is_reply(self, obj):
        return obj.parent_comment_id is not None

    @admin.display(description="Лайки")
    def likes_count(self, obj):
        return obj.likes.count()

    @admin.display(description="Ответов")
    def reply_count(self, obj):
        return obj.replies.count()


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "video", "comment", "liked_at"]
    list_filter = ["liked_at"]
    search_fields = ["user__username"]
    readonly_fields = ["liked_at"]