from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Post(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="user_post")
    content = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    # TODO likes

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.username,
            "content": self.content,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
        }


class Follow(models.Model):
    follower = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="user_follower"
    )
    followed = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="user_followed"
    )
    timestamp = models.DateTimeField(auto_now_add=True)
