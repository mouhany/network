
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("following", views.following, name="following"),
    path("likes", views.likes, name="likes"),
    
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    
    path("create", views.create, name="create"),
    # path("settings", views.settings, name="settings"),
    path("profile/<str:user>", views.profile, name="profile"),
    path("comment/<int:id>", views.comment, name="comment"),
    path("like/<int:id>", views.like, name="like"),
    path("follow/<str:user>", views.follow, name="follow"),
    
    path("post/<int:id>", views.post, name="post"),
    path("edit/<int:id>", views.edit, name="edit"),
    path("delete/<int:id>", views.delete, name="delete"),
]
