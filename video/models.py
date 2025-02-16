from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Video(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='videos')
    name = models.CharField(max_length=255)
    description = models.TextField()
    video = models.FileField(upload_to='video/videos/', validators=[FileExtensionValidator(allowed_extensions=['mp4'])])
    preview = models.ImageField(upload_to='video/previews/')
    date = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='video_likes')
    dislikes = models.ManyToManyField(User, related_name='post_dislikes')
    
    def __str__(self):
        return self.name
