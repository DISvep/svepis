from django.db import models
from post.models import Post
from django.contrib.auth.models import User


# Create your models here.
class PostReaction(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='reactions')
    emoji = models.CharField(max_length=10)
    users = models.ManyToManyField(User, related_name='reactions')
    
    def count(self):
        return self.users.count()
    
    class Meta:
        unique_together = ('post', 'emoji')
    