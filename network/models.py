from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    following = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='followers')
    followers_count = models.IntegerField(default=0)
    following_count = models.IntegerField(default=0)

class Post(models.Model):
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)
    liked_by = models.ManyToManyField(User, related_name='liked_posts')
    dislikes = models.IntegerField(default=0)
