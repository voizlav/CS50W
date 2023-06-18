import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from .models import User, Post, Follow


def index(request):
    return render(request, "network/index.html")


def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(
                request,
                "network/login.html",
                {"message": "Invalid username and/or password."},
            )
    else:
        return render(request, "network/login.html")


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
                request, "network/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request, "network/register.html", {"message": "Username already taken."}
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


@login_required
@csrf_exempt
def newpost(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    try:
        data = json.loads(request.body)
        content = data.get("content", "")
        if not content:
            return JsonResponse({"error": "Empty post."}, status=400)
        if len(content) > 255:
            return JsonResponse({"error": "Post is too long."}, status=400)
    except json.JSONDecodeError:
        return JsonResponse({"error": "JSON data required."}, status=400)
    post = Post()
    post.user = request.user
    post.content = content
    post.save()
    return JsonResponse({"message": "Post added successfully."}, status=201)


def posts(request):
    if request.method != "GET":
        return JsonResponse({"error": "GET request required."}, status=400)
    result = list(reversed([post.serialize() for post in Post.objects.all()]))
    return JsonResponse(result, safe=False)


def login_status(request):
    if request.user.is_authenticated:
        return JsonResponse({"logged_in": True})

    return JsonResponse({"logged_in": False})


@login_required
@csrf_exempt
def follow(request, user_id):
    if request.method != "POST":
        return JsonResponse({"error": "GET request required"}, status=400)
    if request.user.id == user_id:
        return JsonResponse({"error": "Cannot follow yourself"}, status=400)
    try:
        follower = User.objects.get(id=request.user.id)
        followed = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse({"error": "User does not exist"}, status=400)
    if Follow.objects.filter(follower=follower, followed=followed).exists():
        return JsonResponse({"error": "Already following this user."}, status=400)
    follow = Follow(follower=follower, followed=followed)
    follow.save()
    return JsonResponse({"message": "User followed successfully."}, status=201)


@login_required
@csrf_exempt
def unfollow(request, user_id):
    if request.method != "POST":
        return JsonResponse({"error": "GET request required"}, status=400)
    if request.user.id == user_id:
        return JsonResponse({"error": "Cannot unfollow yourself"}, status=400)
    follow = Follow.objects.filter(follower=request.user.id, followed=user_id)
    if not follow.exists():
        return JsonResponse({"error": "You are not following this user."}, status=400)
    follow.delete()
    return JsonResponse({"message": "User unfollowed successfully."}, status=201)


@login_required
def following(request):
    follower = User.objects.get(id=request.user.id)
    followed = [user.followed for user in follower.user_follower.all()]
    posts = Post.objects.filter(user__in=followed)
    result = [post.serialize() for post in posts]
    return JsonResponse(result, safe=False)
