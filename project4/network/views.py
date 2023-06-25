import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, Http404
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


from .models import User, Post, Follow, Like


def index(request):
    result = list(reversed([post.serialize() for post in Post.objects.all()]))
    p = Paginator(result, 10)
    try:
        page_num = request.GET.get("page", 1)
        page = p.page(page_num)
    except PageNotAnInteger:
        page = p.page(1)
    except EmptyPage:
        page = p.page(p.num_pages)
    return render(request, "network/index.html", {"page": page, "all_posts": True})


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
    unfollow = Follow.objects.filter(follower=follower, followed=followed)
    if unfollow.exists():
        unfollow.delete()
        return JsonResponse({"message": "User unfollowed successfully."}, status=201)
    follow = Follow(follower=follower, followed=followed)
    follow.save()
    return JsonResponse({"message": "User followed successfully."}, status=201)


@login_required
def following(request):
    follower = User.objects.get(id=request.user.id)
    followed = [user.followed for user in follower.user_follower.all()]
    posts = [post.serialize() for post in Post.objects.filter(user__in=followed)]
    posts = list(reversed(sorted(posts, key=lambda post: post["id"])))
    p = Paginator(posts, 10)
    page_num = request.GET.get("page", 1)
    page = p.page(page_num)
    return render(request, "network/index.html", {"page": page})


@login_required
@csrf_exempt
def like(request, post_id):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    try:
        liker = User.objects.get(id=request.user.id)
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post does not exist"}, status=400)
    for like in liker.user_like.all():
        if like.post.id == post.id:
            like.delete()
            return JsonResponse({"message": "Post unliked successfully."}, status=201)
    liked = Like(like=liker, post=post)
    liked.save()
    return JsonResponse({"message": "Post liked successfully."}, status=201)


@login_required
def likes(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
        likes = post.post_like.all()
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post does not exist"}, status=400)
    likes = [user.like.username for user in likes]
    return JsonResponse({"likes": likes}, status=200)


@login_required
@csrf_exempt
def edit(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post does not exist."}, status=400)
    if request.user != post.user:
        return JsonResponse({"error": "Forbidden."}, status=400)
    try:
        data = json.loads(request.body)
        content = data.get("content", "")
        if not content:
            return JsonResponse({"error": "Empty post."}, status=400)
        if len(content) > 255:
            return JsonResponse({"error": "Post is too long."}, status=400)
    except json.JSONDecodeError:
        return JsonResponse({"error": "JSON data required."}, status=400)
    post.content = content
    post.edited = True
    post.save()
    return JsonResponse({"content": post.content})


def profile(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise Http404("User doesn't exist.")
    posts = list(reversed([post.serialize() for post in user.user_post.all()]))
    p = Paginator(posts, 10)
    try:
        page = p.page(request.GET.get("page", 1))
    except PageNotAnInteger:
        page = p.page(1)
    except EmptyPage:
        page = p.page(p.num_pages)
    follower = user.user_follower.all()
    followed = user.user_followed.all()
    return render(
        request,
        "network/index.html",
        {"page": page, "follower": follower, "followed": followed, "profile": username},
    )
