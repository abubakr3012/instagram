from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.db.models import Q
from .models import User, Profile, Follow

UserModel = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            phone=validated_data['phone'],
            password=validated_data['password'],
        )
        Profile.objects.create(user=user)
        return user

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': UserSerializer(instance).data,
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone']


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    posts_cnt = serializers.SerializerMethodField()
    is_following = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = [
            'id',
            'user_id',
            'username',
            'email',
            'image',
            'follower_cnt',
            'following_cnt',
            'videos_cnt',
            'posts_cnt',
            'bio',
            'is_following',
        ]
        read_only_fields = [
            'follower_cnt',
            'following_cnt',
            'videos_cnt',
            'posts_cnt',
            'is_following',
        ]

    def get_posts_cnt(self, obj):
        return obj.user.posts.count()

    def get_is_following(self, obj):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return False
        if obj.user_id == request.user.id:
            return False
        return Follow.objects.filter(
            follower=request.user,
            following=obj.user,
        ).exists()

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get('request')
        if request:
            if instance.image:
                data['image'] = request.build_absolute_uri(instance.image.url)
        return data


class FollowUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    image = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ['user_id', 'username', 'image', 'bio']

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None
