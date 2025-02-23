from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import User
from django.conf import settings
from django.db import models
import os


# Create your models here.
class Video(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='videos')
    name = models.CharField(max_length=255)
    description = models.TextField()
    video = models.FileField(upload_to='video/videos/', validators=[FileExtensionValidator(allowed_extensions=['mp4'])])
    preview = models.ImageField(upload_to='video/previews/')
    date = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='video_likes', null=True, blank=True)
    dislikes = models.ManyToManyField(User, related_name='post_dislikes', null=True, blank=True)
    
    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        if self.preview:
            preview_path = os.path.join(settings.MEDIA_ROOT, str(self.preview))
            if os.path.exists(preview_path):
                os.remove(preview_path)
                
        if self.video:
            video_path = os.path.join(settings.MEDIA_ROOT, str(self.video))
            if os.path.exists(video_path):
                os.remove(video_path)
        
        super().delete(*args, **kwargs)
