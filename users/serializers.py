from rest_framework import serializers
from .models import User, Profile

class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True
    )


    class Meta:

        model = User

        fields = [
            "username",
            "email",
            "phone",
            "password"
        ]


    def create(self, validated_data):

        user = User.objects.create_user(

            username=validated_data["username"],

            email=validated_data["email"],

            phone=validated_data["phone"],

            password=validated_data["password"]

        )


        Profile.objects.create(
            user=user
        )


        return user

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "phone",
        ]


class ProfileSerializer(serializers.ModelSerializer):

    username = serializers.CharField(
        source="user.username",
        read_only=True
    )

    email = serializers.EmailField(
        source="user.email",
        read_only=True
    )


    class Meta:
        model = Profile

        fields = [
            "id",
            "username",
            "email",
            "image",
            "follower_cnt",
            "following_cnt",
            "videos_cnt",
            "bio",
        ]