from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("item/<int:item_id>", views.items, name="item"),
    path("item/<int:item_id>/close", views.close_item, name="close_item"),
    path("item/<int:item_id>/bid", views.bid_item, name="bid_item"),
    path("item/<int:item_id>/comment", views.comment_item, name="comment_item"),
    path("watchlist/<int:item_id>/add", views.watchlist_add, name="watchlist_add"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("category/<str:name>", views.categories, name="categories"),
    path("category", views.category, name="category"),
]
