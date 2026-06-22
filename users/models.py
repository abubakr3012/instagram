from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=16, unique=True)

    def __str__(self):
        return self.username


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_image/', blank=True, null=True)
    follower_cnt = models.PositiveIntegerField(default=0)
    following_cnt = models.PositiveIntegerField(default=0)
    videos_cnt = models.PositiveIntegerField(default=0)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}->{self.user.email}"


class Follow(models.Model):
    follower = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='following_relations'
    )
    following = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='follower_relations'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['follower', 'following'],
                name='unique_follow',
            ),
        ]

    def __str__(self):
        return f"{self.follower.username} -> {self.following.username}"
