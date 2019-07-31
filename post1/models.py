from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Post(models.Model):
    title = models.CharField(max_length=100, default="")
    content = models.TextField(default="")
    pub_date = models.DateTimeField(default = timezone.now)
    def __str__(self):
        return self.title

class Account(models.Model):
    # 장고 유저와 내가 만든 모델 1대1 연결
    user  = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField()
    nickname = models.CharField(max_length=20)
    def __str__(self):
        return self.user.username
        
class Meta:
    ordering = ['-id']
