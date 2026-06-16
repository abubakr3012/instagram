from django.db import models
from django.contrib.auth import get_user_model

User=get_user_model()

class Videos(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField(max_length=50)
    file=models.FileField(upload_to='media/videos/')
    likes_cnt=models.PositiveIntegerField(default=0)
    views_cnt=models.PositiveIntegerField(default=0)
    comment_cnt=models.PositiveIntegerField(default=0)
    created_at=models.DateTimeField(auto_now_add=True)
    is_deleted=models.BooleanField(default=False)

    

    def __str__(self):
        return f'{self.user.username}-> {self.title}'

class Reposts(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    video=models.ForeignKey(Videos,on_delete=models.CASCADE)
    reposted_at=models.DateTimeField(auto_now_add=True)
    is_deleted=models.BooleanField(default=False)

    class Meta:
        unique_together = ['user', 'video']

    def __str__(self):
        return f'{self.user.username}-> {self.video.title}'

class SavedVideos(models.Model):

    user=models.ForeignKey(User,on_delete=models.CASCADE)
    video=models.ForeignKey(Videos,on_delete=models.CASCADE)
    saved_at=models.DateTimeField(auto_now_add=True)
    is_deleted=models.BooleanField(default=False)

    class Meta:
        unique_together = ['user', 'video']

    def __str__(self):
        return f'{self.user.username}-> {self.video.title}'