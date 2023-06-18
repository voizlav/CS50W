from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("login_status", views.login_status, name="login_status"),
    path("register", views.register, name="register"),
    path("newpost", views.newpost, name="newpost"),
    path("posts", views.posts, name="posts"),
    path("follow/<int:user_id>", views.follow, name="follow"),
    path("unfollow/<int:user_id>", views.unfollow, name="unfollow"),
    path("following", views.following, name="following"),
]
