from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator


class User(AbstractUser):
    pass


class Auction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=20)
    description = models.CharField(max_length=1000)
    starting_bid = models.IntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(2147483647)]
    )
    category = models.CharField(blank=True, max_length=30)
    hyperlink = models.URLField(blank=True, max_length=200)
    time = models.TimeField(default=timezone.now().time())
    active = models.BooleanField(default=True)


class Bids:
    # TODO
    pass


class Comments:
    # TODO
    pass
