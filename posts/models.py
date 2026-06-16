from django.db import models
from django.contrib.auth import get_user_model

User=get_user_model()

class Post(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    photo=models.ImageField(upload_to='posts/')
    music=models.FileField(upload_to='musics/',blank=True,null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'{self.user.username}'