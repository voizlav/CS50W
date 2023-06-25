from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newpost", views.newpost, name="newpost"),
    path("posts", views.posts, name="posts"),
    path("follow/<int:user_id>", views.follow, name="follow"),
    path("unfollow/<int:user_id>", views.unfollow, name="unfollow"),
    path("following", views.following, name="following"),
    path("like/<int:post_id>", views.like, name="like"),
    path("likes/<int:post_id>", views.likes, name="likes"),
    path("edit/<int:post_id>", views.edit, name="edit"),
    path("profile/<str:username>", views.profile, name="profile"),
]
