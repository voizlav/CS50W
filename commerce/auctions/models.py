from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Auction(models.Model):
    title = models.CharField(max_length=20)
    description = models.CharField(max_length=1000)
    starting_bid = models.IntegerField(default=0)
    category = models.CharField(blank=True, max_length=30)
    hyperlink = models.URLField(blank=True, max_length=200)


class Bids:
    # TODO
    pass


class Comments:
    # TODO
    pass
