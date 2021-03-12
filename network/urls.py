
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new", views.new, name="new"),
    path("all", views.all, name="all"),
    path("users/<int:user>", views.profile, name="profile"),
    path("following", views.following, name="following"),
    path("edit", views.edit, name="edit"),
    path("follow/<int:user>", views.follow, name="follow"),
    path("like/<int:post_id>", views.like, name="like")
]
