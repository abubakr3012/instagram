from rest_framework import serializers
from .models import Videos, Reposts, SavedVideos


class VideoSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Videos
        fields = ['id', 'user', 'title', 'file', 'likes_cnt', 
                  'views_cnt', 'comment_cnt', 'created_at', 'is_deleted']
        read_only_fields = ['likes_cnt', 'views_cnt', 'comment_cnt', 
                            'created_at', 'is_deleted']


class VideoCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Videos
        fields = ['title', 'file']


class RepostSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    video = VideoSerializer(read_only=True)
    video_id = serializers.PrimaryKeyRelatedField(
        queryset=Videos.objects.filter(is_deleted=False),
        write_only=True,
        source='video'
    )

    class Meta:
        model = Reposts
        fields = ['id', 'user', 'video', 'video_id', 'reposted_at', 'is_deleted']
        read_only_fields = ['reposted_at', 'is_deleted']


class SavedVideoSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    video = VideoSerializer(read_only=True)
    video_id = serializers.PrimaryKeyRelatedField(
        queryset=Videos.objects.filter(is_deleted=False),
        write_only=True,
        source='video'
    )

    class Meta:
        model = SavedVideos
        fields = ['id', 'user', 'video', 'video_id', 'saved_at', 'is_deleted']
        read_only_fields = ['saved_at', 'is_deleted']