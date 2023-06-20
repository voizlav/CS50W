from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Post(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="user_post")
    content = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.username,
            "content": self.content,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "edited": self.edited,
        }


class Like(models.Model):
    like = models.ForeignKey("User", on_delete=models.CASCADE, related_name="user_like")
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="post_like")


class Follow(models.Model):
    follower = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="user_follower"
    )
    followed = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="user_followed"
    )
    timestamp = models.DateTimeField(auto_now_add=True)
