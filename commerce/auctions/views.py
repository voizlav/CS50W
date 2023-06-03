from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.db.models import Max
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse
from django import forms
from .models import Auction, User, Bids, Comments, Watchlist


class AuctionForm(forms.ModelForm):
    class Meta:
        model = Auction
        fields = ["title", "description", "starting_bid", "category", "hyperlink"]


class BidForm(forms.Form):
    bid_amount = forms.IntegerField()


class CommentForm(forms.Form):
    comment = forms.CharField(max_length=1000)


def index(request):
    all_listing = Auction.objects.filter(active=True).annotate(bid=Max("bids__amount"))
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
        msg = "Invalid form."
        messages.add_message(request, messages.WARNING, msg)
        redirect("create")
    return render(request, "auctions/create.html", {"form": AuctionForm()})


def items(request, item_id):
    item = get_object_or_404(Auction, id=item_id)
    all_bids = item.bids.all()
    bid = item.bids.latest("timestamp")
    all_comments = item.comment.all()
    messages.get_messages(request)
    return render(
        request,
        "auctions/items.html",
        {"item": item, "bid": bid, "all_bids": all_bids, "all_comments": all_comments},
    )


@login_required
def close_item(request, item_id):
    item = get_object_or_404(Auction, id=item_id)
    bid = item.bids.latest("timestamp")
    if request.method == "POST":
        if request.user.is_authenticated and request.user == item.user:
            item.active = False
            item.winner = bid.user
            item.save()
            return HttpResponseRedirect(reverse("item", args=[item_id]))
        return HttpResponse("Unauthorized", status=401)
    return HttpResponseRedirect(reverse("item", args=[item_id]))


@login_required
def bid_item(request, item_id):
    item = get_object_or_404(Auction, id=item_id)
    latest_bid = item.bids.latest("timestamp")
    if request.method == "POST":
        if not request.user.is_authenticated:
            return HttpResponse("Unauthorized", status=401)
        form = BidForm(request.POST)
        if form.is_valid():
            if item.active:
                bid_amount = form.cleaned_data["bid_amount"]
                if bid_amount > latest_bid.amount:
                    bid = Bids()
                    bid.auction = item
                    bid.user = request.user
                    bid.amount = bid_amount
                    bid.save()
                    return HttpResponseRedirect(reverse("item", args=[item_id]))
                msg = "Please provide a higher bid to place a valid offer."
                messages.add_message(request, messages.WARNING, msg)
                return redirect("item", item_id=item_id)
            msg = "The auction you are trying to bid is closed."
            messages.add_message(request, messages.WARNING, msg)
            return redirect("item", item_id=item_id)
        msg = "Invalid bid amount."
        messages.add_message(request, messages.WARNING, msg)
        return redirect("item", item_id=item_id)
    return HttpResponseRedirect(reverse("item", args=[item_id]))


@login_required
def comment_item(request, item_id):
    item = get_object_or_404(Auction, id=item_id)
    latest_bid = item.bids.latest("timestamp")
    all_bids = item.bids.all()
    if request.method == "POST":
        if not request.user.is_authenticated:
            return HttpResponse("Unauthorized", status=401)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comments()
            comment.content = form.cleaned_data["comment"]
            comment.user = request.user
            comment.auction = item
            comment.save()
            return HttpResponseRedirect(reverse("item", args=[item_id]))
        msg = "Invalid comment."
        messages.add_message(request, message.WARNING, msg)
        return redirect("item", item_id=item_id)
    return HttpResponseRedirect(reverse("item", args=[item_id]))


@login_required
def watchlist_add(request, item_id):
    item = get_object_or_404(Auction, id=item_id)
    if request.method == "POST":
        watch = Watchlist()
        watch.auction = item
        watch.user = request.user
        watch.save()
        return HttpResponseRedirect(reverse("item", args=[item_id]))
    return HttpResponseRedirect(reverse("item", args=[item_id]))
