from rest_framework import serializers
from .models import Post


class PostSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Post
        fields = (
            "id",
            "user",
            "photo",
            "music",
            "created_at",
        )
        read_only_fields = ("id", "user", "created_at")

    def create(self, validated_data):
        request = self.context.get("request")
        post = Post.objects.create(user=request.user, **validated_data)
        return post

class PostMusicSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ("music",)