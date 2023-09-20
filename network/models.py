from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass
    date_joined = models.DateTimeField(auto_now_add=True)
    following = models.ManyToManyField("self", blank=True, related_name="followers", symmetrical=False)
    
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