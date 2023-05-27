from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django import forms
from .models import Auction, User


class AuctionForm(forms.ModelForm):
    class Meta:
        model = Auction
        fields = ["title", "description", "starting_bid", "category", "hyperlink"]


class BidForm(forms.Form):
    bid_amount = forms.IntegerField()


def index(request):
    all_listing = Auction.objects.filter(active=True)
    return render(request, "auctions/index.html", {"all_listing": all_listing})


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        return render(
            request,
            "auctions/login.html",
            {"message": "Invalid username and/or password."},
        )
    return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(
                request, "auctions/register.html", {"message": "Passwords must match."}
            )
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request,
                "auctions/register.html",
                {"message": "Username already taken."},
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required
def create(request):
    if request.method == "POST":
        form = AuctionForm(request.POST)
        if form.is_valid():
            new_auction = Auction()
            new_auction.user = request.user
            new_auction.title = form.cleaned_data["title"]
            new_auction.description = form.cleaned_data["description"]
            if form.cleaned_data["category"]:
                new_auction.category = form.cleaned_data["category"]
            if form.cleaned_data["hyperlink"]:
                new_auction.hyperlink = form.cleaned_data["hyperlink"]
            new_auction.save()
            bid = Bids()
            bid.user = request.user
            if form.cleaned_data["starting_bid"]:
                bid.amount = form.cleaned_data["starting_bid"]
            bid.auction = new_auction
            bid.save()
            return HttpResponseRedirect(reverse("index"))
        return render(request, "auctions/create.html", {"message": "Invalid form."})
    return render(request, "auctions/create.html", {"form": AuctionForm()})


def items(request, item_id):
    item = get_object_or_404(Auction, id=item_id)
    return render(request, "auctions/items.html", {"item": item})


@login_required
def close_item(request, item_id):
    item = get_object_or_404(Auction, id=item_id)
    if request.method == "POST":
        if request.user.is_authenticated and request.user == item.user:
            item.active = False
            item.save()
            return HttpResponseRedirect(reverse("item", args=[item_id]))
        return HttpResponse("Unauthorized", status=401)
    return HttpResponseRedirect(reverse("item", args=[item_id]))


@login_required
def bid_item(request, item_id):
    item = get_object_or_404(Auction, id=item_id)
    if request.method == "POST":
        if not request.user.is_authenticated:
            return HttpResponse("Unauthorized", status=401)
        form = BidForm(request.POST)
        if form.is_valid():
            if item.active:
                bid_amount = form.cleaned_data["bid_amount"]
                print("BID DEBUG:", bid_amount)
                # TODO Implement bid class model

                return HttpResponseRedirect(reverse("item", args=[item_id]))
            return HttpResponse("Inactive item", status=400)
        return HttpResponse("Invalid bid", status=400)
    return HttpResponseRedirect(reverse("item", args=[item_id]))
