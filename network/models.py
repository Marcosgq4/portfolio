from django.conf import settings
from django.db import models

    
class New_Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="posts")
    content = models.TextField(max_length=500) 
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_posts', blank=True)

    def __str__(self):
        return f"{self.user.username}: {self.content[:50]}"
    
    @property
    def num_likes(self):
        return self.likes.count()
    
class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    followers = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="followers_of", symmetrical=False)
    following = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="following_of", symmetrical=False)

    def __str__(self):
        return self.user.username
