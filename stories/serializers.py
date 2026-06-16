from rest_framework import serializers
from .models import Stories, Actualnost, Archive


class StoriesSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    is_expired = serializers.SerializerMethodField()

    class Meta:
        model = Stories
        fields = [
            'id', 'user', 'file', 'created_at', 'expires_at',
            'likes_cnt', 'views_cnt', 'is_deleted', 'is_expired',
        ]
        read_only_fields = ['id', 'created_at', 'likes_cnt', 'views_cnt']

    def get_is_expired(self, obj):
        from django.utils import timezone
        return obj.expires_at < timezone.now()

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
    
class ActualnostSerializer(serializers.ModelSerializer):
    stories = StoriesSerializer(many=True, read_only=True)

    stories_id = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Stories.objects.filter(is_deleted=False),
        source='stories',
        write_only=True
    )

    class Meta:
        model = Actualnost
        fields = ['id', 'name', 'stories', 'stories_id', 'is_deleted', 'created_at']
        read_only_fields = ['id', 'created_at']

class ArchiveSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Archive
        fields = ['id', 'user', 'video', 'stories', 'archived_at']
        read_only_fields = ['id', 'archived_at', 'user']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)