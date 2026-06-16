from django.db import models
from django.contrib.auth import get_user_model
from videos.models import Videos
User = get_user_model()


class Stories(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,default=1
    )
    file = models.FileField(upload_to='media/stories/')
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    likes_cnt = models.PositiveIntegerField(default=0)
    views_cnt = models.PositiveIntegerField(default=0)

    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} -> {self.file.name}'


class Actualnost(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,default=1
    )

    name = models.CharField(max_length=20)

    stories = models.ManyToManyField(
        Stories,
        related_name='actualnost'
    )

    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name
class Archive(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,default=1)
    video=models.ForeignKey(Videos,on_delete=models.CASCADE)
    stories=models.ForeignKey(Stories,on_delete=models.CASCADE)
    archived_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
