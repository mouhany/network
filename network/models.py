from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Count


class User(AbstractUser):
    pass
    date_joined = models.DateTimeField(auto_now_add=True)
    following = models.ManyToManyField("self", blank=True, related_name="followers", symmetrical=False)
        
    def num_of_following(self):
        return len(self.following.all())
    
    def num_of_followers(self):
        return len(self.followers.all())
    
    def most_followed_users():
        users = User.objects.annotate(follower_count=Count('followers'))
        return users.order_by('-follower_count')
        
    def __str__(self):
        return f"{self.id}. {self.username}"

class Post(models.Model):
    content = models.CharField(max_length=255)
    poster = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    likers = models.ManyToManyField(User, blank=True, related_name="likes")
    date_posted = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)
    
    def num_of_likes(self):
        return len(self.likers.all())
    
    def num_of_comments(self):
        return len(self.comments.all())
    
    def most_liked_posts():
        posts = Post.objects.annotate(likes_count=Count('likers'))
        return posts.order_by('-likes_count')
    
    def most_commented_posts():
        posts = Post.objects.annotate(comment_count=Count('comments'))
        return posts.order_by('-comment_count')
    
    def __str__(self):
        return f"Post#{self.id} - {self.poster.username}: {self.content}"
    
    class Meta:
        ordering = ["-date_posted"]
        
class Comment(models.Model):
    main_post = models.ForeignKey(Post, on_delete=models.SET_DEFAULT, default="Post deleted.", related_name="comments")
    comment = models.CharField(max_length=255)
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commenter")
    commented = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Post#{self.main_post.id} - {self.commenter.username}: {self.comment}"
    
    class Meta:
        ordering = ["-commented"]