from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone, datetime_safe
from django.core.validators import MinValueValidator, MaxValueValidator


CATEGORIES = [
    ("F", "fashion"),
    ("T", "toys"),
    ("E", "electronics"),
    ("H", "home"),
    ("O", "other"),
]


class User(AbstractUser):
    pass


class Auction(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="auction_creator"
    )
    winner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="auction_winner",
    )
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    starting_bid = models.IntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(2147483647)]
    )
    category = models.CharField(blank=True, max_length=30, choices=CATEGORIES)
    hyperlink = models.URLField(
        default="/static/img/noimage.png", blank=True, max_length=200
    )
    time = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)


class Bids(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="bids")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.IntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(2147483647)]
    )
    timestamp = models.DateTimeField(auto_now_add=True)


class Comments(models.Model):
    auction = models.ForeignKey(
        Auction, on_delete=models.CASCADE, related_name="comment"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=1000)
    timestamp = models.DateTimeField(auto_now_add=True)


class Watchlist(models.Model):
    auction = models.ForeignKey(
        Auction, on_delete=models.CASCADE, related_name="watching_auction"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="watching_user"
    )
