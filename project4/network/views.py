import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from .models import User, Post


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
