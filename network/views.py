from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.paginator import Paginator

from .models import User, Post, Comment


def index(request):
    posts = Post.objects.all()
    
    p = Paginator(posts, 4) # Will set to 10 posts later
    page_number = request.GET.get("page")
    page_posts = p.get_page(page_number)
    
    return render(request, "network/index.html", {
        "posts": page_posts,
        "page_number": page_number,
        "headline": "Home"
    })


def profile(request, username):
    username = User.objects.get(username=username)
    return render(request, "network/index.html", {
        "posts": Post.objects.filter(poster=username),
        "headline": f"Profile: {username.username}"
    })


def create(request):
    # New post must be via POST request
    if request.method != "POST":
        return JsonResponse({
            "error": "POST request required."
        }, status=400)
    
    content = request.POST["content"]
    new_post = Post(
        content=content,
        poster=request.user)
    new_post.save()
    return redirect("index")


def comment(request, id):
    if request.method != "POST":
        return JsonResponse({
            "error": "POST request required."
        }, status=400)
    main_post = Post.objects.get(pk=id)
    comment = request.POST['comment']
    new_comment = Comment(
        main_post=main_post, 
        comment=comment, 
        commenter=request.user
    )
    new_comment.save()
    return redirect("index")

# todo
def like(request, id):
    if request.method == "POST":
        post = Post.objects.get(pk=id)
        posts_liked = request.user.likes.all()
        if post in posts_liked:
            post.likers.remove(request.user)
        else:
            post.likers.add(request.user)
        return redirect("index")

# todo
def edit(request, id):
    # Edit post must be via POST request
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    pass


################################################

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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
