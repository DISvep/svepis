from django.db import models
from django.contrib.auth.models import User


class Widget(models.Model):
    WIDGET_TYPES = [
        ('text', 'Text'),
        ('image', 'Image'),
        ('video', 'Video')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='widgets')
    widget_type = models.CharField(max_length=50, choices=WIDGET_TYPES)
    x_position = models.IntegerField(default=0)
    y_position = models.IntegerField(default=0)
    width = models.IntegerField(default=100)
    height = models.IntegerField(default=100)
    z_index = models.IntegerField(default=1)
    content = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='widget_images/', blank=True, null=True)
    
    def __str__(self):
        return f"{self.widget_type} - {self.user.username}"
    