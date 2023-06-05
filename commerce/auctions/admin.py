from django.contrib import admin
from .models import Auction, Comments, Bids

admin.site.register(Auction)
admin.site.register(Comments)
admin.site.register(Bids)
