from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Post(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="user_post")
    content = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    # TODO likes
