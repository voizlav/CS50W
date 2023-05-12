from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from .models import Auction, User


class AuctionForm(forms.ModelForm):
    class Meta:
        model = Auction
        fields = ["title", "description", "starting_bid", "category", "hyperlink"]


def index(request):
    return render(request, "auctions/index.html")


def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
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

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(
                request, "auctions/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
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
            if form.cleaned_data["starting_bid"]:
                new_auction.starting_bid = form.cleaned_data["starting_bid"]
            if form.cleaned_data["category"]:
                new_auction.category = form.cleaned_data["category"]
            if form.cleaned_data["hyperlink"]:
                new_auction.hyperlink = form.cleaned_data["hyperlink"]
            new_auction.save()
            return render(request, "auctions/index.html")
    return render(request, "auctions/create.html", {"form": AuctionForm()})
