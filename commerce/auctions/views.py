from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from .models import Auction


class AuctionForm(forms.ModelForm):
    class Meta:
        model = Auction
        fields = "__all__"
        widgets = {
            "description": forms.TextInput(
                attrs={
                    "autofocus": True,
                    "placeholder": "Description",
                    "class": "form-control",
                }
            ),
            "starting_bid": forms.NumberInput(
                attrs={
                    "placeholder": 0,
                    "class": "form-control",
                },
            ),
            "category": forms.TextInput(
                attrs={
                    "placeholder": "Category",
                    "class": "form-control",
                },
            ),
            "hyperlink": forms.TextInput(
                attrs={
                    "placeholder": "Link",
                    "class": "form-control",
                },
            ),
        }
        labels = {
            "title": "",
            "description": "",
            "starting_bid": "",
            "category": "",
            "hyperlink": "",
        }
        label_suffix = ""


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


def create(request):
    if request.method == "POST":
        ...

    return render(request, "auctions/create.html", {"form": AuctionForm()})
