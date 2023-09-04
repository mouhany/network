from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass
    following = models.ManyToManyField("self", blank=True, related_name="followers", symmetrical=False)
    

class Post(models.Model):
    content = models.CharField(max_length=255)
    poster = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    likers = models.ManyToManyField(User, blank=True, related_name="likes")
    date_posted = models.DateTimeField(auto_now_add=True)
    
    def num_of_likes(self):
        return self.likers.all().count()
    
    class Meta:
        ordering = ["-date_posted"]