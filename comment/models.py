from django.contrib.auth.models import User
from video.models import Video
from post.models import Post
from django.db import models


# Create your models here.
class PostComment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)


class VideoComment(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='video_comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='video_comments')
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
