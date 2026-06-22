from rest_framework import serializers
from .models import Post, PostLike, PostComment


class PostCommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    user_id = serializers.IntegerField(source='user.id', read_only=True)

    class Meta:
        model = PostComment
        fields = ['id', 'user', 'user_id', 'text', 'created_at']
        read_only_fields = ['id', 'user', 'user_id', 'created_at']


class PostSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = (
            'id',
            'user',
            'user_id',
            'photo',
            'caption',
            'music',
            'likes_count',
            'comments_count',
            'is_liked',
            'comments',
            'created_at',
        )
        read_only_fields = ('id', 'user', 'user_id', 'created_at')

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_comments_count(self, obj):
        return obj.comments.filter(is_deleted=False).count()

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(user=request.user).exists()
        return False

    def get_comments(self, obj):
        if not self.context.get('include_comments'):
            return None
        comments = obj.comments.filter(is_deleted=False).select_related('user')[:50]
        return PostCommentSerializer(comments, many=True).data

    def create(self, validated_data):
        request = self.context.get('request')
        return Post.objects.create(user=request.user, **validated_data)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get('request')
        if request and instance.photo:
            data['photo'] = request.build_absolute_uri(instance.photo.url)
        if request and instance.music:
            data['music'] = request.build_absolute_uri(instance.music.url)
        return data


class PostMusicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('music',)
