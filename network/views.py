from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.paginator import Paginator
import json

from .models import User, Post, Comment


def index(request):
    most_followed_users = User.most_followed_users()
    most_liked_posts = Post.most_liked_posts()
    most_commented_posts = Post.most_commented_posts()
    
    posts = Post.objects.all()
    
    p = Paginator(posts, 10) # Will set to 10 posts later
    page_number = request.GET.get("page")
    page_posts = p.get_page(page_number)
    
    return render(request, "network/index.html", {
        "most_followed_users": most_followed_users,
        "most_liked_posts": most_liked_posts,
        "most_commented_posts": most_commented_posts,
        "posts": page_posts,
        "page_number": page_number,
    })


def following(request):
    most_followed_users = User.most_followed_users()
    most_liked_posts = Post.most_liked_posts()
    most_commented_posts = Post.most_commented_posts()
    
    followed_user = User.objects.get(username=request.user.username).following.all()
    followed_posts = Post.objects.filter(poster__in=followed_user)
    
    p = Paginator(followed_posts, 10)  # Will set to 10 posts later
    page_number = request.GET.get("page")
    followed_user_posts = p.get_page(page_number)
    
    return render(request, "network/index.html", {
        "most_followed_users": most_followed_users,
        "most_liked_posts": most_liked_posts,
        "most_commented_posts": most_commented_posts,
        "posts": followed_user_posts,
    })


def likes(request):
    most_followed_users = User.most_followed_users()
    most_liked_posts = Post.most_liked_posts()
    most_commented_posts = Post.most_commented_posts()
    
    profile = User.objects.get(username=request.user.username)
    liked_post = profile.likes.all()
    # Shorter ver.
    # liked_post = User.objects.get(pk=request.user.id).likes.all()

    p = Paginator(liked_post, 10)  # Will set to 10 posts later
    likes_page_number = request.GET.get("page")
    likes_page_posts = p.get_page(likes_page_number)

    return render(request, "network/index.html", {
        "most_followed_users": most_followed_users,
        "most_liked_posts": most_liked_posts,
        "most_commented_posts": most_commented_posts,
        "posts": likes_page_posts,
        "page_number": likes_page_number,
    })


def profile(request, user):
    most_followed_users = User.most_followed_users()
    most_liked_posts = Post.most_liked_posts()
    most_commented_posts = Post.most_commented_posts()
    
    profile = User.objects.get(username=user)
    profile_posts = Post.objects.filter(poster=profile)
    profile_likes = Post.objects.filter(likers=profile)
    profile_comments = Comment.objects.filter(commenter=profile)
    
    # Check if profile is followed by request.user
    if request.user.is_authenticated and profile in request.user.following.all():
        is_followed = True
    else:
        is_followed = False
    
    return render(request, "network/profile.html", {
        "most_followed_users": most_followed_users,
        "most_liked_posts": most_liked_posts,
        "most_commented_posts": most_commented_posts,
        "profile": profile,
        "posts": profile_posts,
        "liked_posts": profile_likes,
        "comments": profile_comments,
        "is_followed": is_followed
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
    return redirect("post", id=id)


def post(request, id):
    most_followed_users = User.most_followed_users()
    most_liked_posts = Post.most_liked_posts()
    most_commented_posts = Post.most_commented_posts()
    
    post = Post.objects.get(pk=id)
    post_comments = post.comments.all()
    
    if request.method == "POST":
        comment = request.POST['comment_post']
        new_comment = Comment(
            main_post=post, 
            comment=comment, 
            commenter=request.user
        )
        new_comment.save()
    
    return render(request, "network/post.html", {
        "post": post,
        "post_comments": post_comments,
        "most_followed_users": most_followed_users,
        "most_liked_posts": most_liked_posts,
        "most_commented_posts": most_commented_posts,
    })
    
# todo
def like(request, id):
    # Follow must be via POST request
    if request.method != "POST":
        return JsonResponse({
            "error": "POST request required."
        }, status=400)
        
    post = Post.objects.get(pk=id)
    posts_liked = request.user.likes.all()
    if post in posts_liked:
        post.likers.remove(request.user)
    else:
        post.likers.add(request.user)
    return redirect("index")


def follow(request, user):
    # Follow must be via POST request
    if request.method != "POST":
        return JsonResponse({
            "error": "POST request required."
        }, status=400)
    
    profile = User.objects.get(username=user)
    following_list = request.user.following.all()
    
    if request.user.is_authenticated and profile in following_list:
        # If profile is followed by request.user,
        # clicking on button will remove profile from following_list
        request.user.following.remove(profile)
    else:
        request.user.following.add(profile)
    return redirect("profile", user=profile.username)

# done but need to incorporate js for better ux 
def edit(request, id):
    # Edit post must be via POST request
    if request.method != "POST":
        return JsonResponse({
            "error": "POST request required."
        }, status=400)
    
    # Get current post
    post = Post.objects.get(pk=id)
    
    # Get new content for current post
    data = json.loads(request.body)
    
    # Save new content to current post
    post.content = data["content"]
    post.edited = True
    post.save()
    
    return JsonResponse({
        "success": True, 
        "message": "(edited)", 
        "data": data["content"]
        }, status=201)
    
    # edited_content = request.POST["edited_content"]
    # edit_post = Post.objects.filter(pk=id).update(content=edited_content, edited=True)
    # return redirect("index")


# def delete(request, id):
#     if request.method != "POST":
#         return JsonResponse({
#             "error": "POST request required."
#         }, status=400)
#     try:
#         post = Post.objects.get(pk=id)
#         if request.user == post.poster.username:
#             post.delete()
#         return JsonResponse({
#             "success": True,
#             "message": "Post deleted"
#         }, status=201)
#     except:
#         return JsonResponse({
#             "success": False,
#             "message": "You don't have permission to do this."
#         }, status=403)

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
