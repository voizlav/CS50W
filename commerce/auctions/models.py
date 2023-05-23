from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone, datetime_safe
from django.core.validators import MinValueValidator, MaxValueValidator


class User(AbstractUser):
    pass


class Auction(models.Model):
    CATEGORIES = [
        ("F", "fashion"),
        ("T", "toys"),
        ("E", "electronics"),
        ("H", "home"),
        ("O", "other"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    starting_bid = models.IntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(2147483647)]
    )
    category = models.CharField(blank=True, max_length=30, choices=CATEGORIES)
    hyperlink = models.URLField(
        default="/static/img/noimage.jpg", blank=True, max_length=200
    )
    time = models.DateTimeField(default=timezone.now)
    active = models.BooleanField(default=True)


class Bids:
    # TODO
    pass


class Comments:
    # TODO
    pass
