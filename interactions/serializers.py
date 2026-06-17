from rest_framework import serializers
from .models import Comment, Like

class ReplySerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            "id", "user", "comment_text", "photo",
            "likes_count", "is_deleted", "created_at",
        ]
        read_only_fields = ["id", "user", "is_deleted", "created_at"]

    def get_likes_count(self, obj):
        return obj.likes.count()


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    replies = ReplySerializer(many=True, read_only=True)
    likes_count = serializers.SerializerMethodField()
    reply_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            "id", "video", "user", "parent_comment",
            "comment_text", "photo", "likes_count", "reply_count",
            "is_liked", "replies", "is_deleted", "created_at",
        ]
        read_only_fields = ["id", "user", "is_deleted", "created_at"]

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_reply_count(self, obj):
        return obj.replies.filter(is_deleted=False).count()

    def get_is_liked(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return obj.likes.filter(user=request.user).exists()
        return False

    def validate(self, attrs):
        parent = attrs.get("parent_comment")
        if parent and parent.parent_comment is not None:
            raise serializers.ValidationError(
            )
        return attrs

class LikeSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Like
        fields = ["id", "video", "comment", "user", "liked_at"]
        read_only_fields = ["id", "user", "liked_at"]

    def validate(self, attrs):
        if not attrs.get("video") and not attrs.get("comment"):
            raise serializers.ValidationError(
            )
        if attrs.get("video") and attrs.get("comment"):
            raise serializers.ValidationError(
            )
        return attrs