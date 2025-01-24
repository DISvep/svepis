from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Portal(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='portal')
    avatar = models.ImageField(
        upload_to='portal/avatar/',
        default='portal/default-avatar.png',
        blank=True,
        null=True
    )
    banner = models.ImageField(
        upload_to='portal/banner/',
        default='portal/default-banner.png',
        blank=True,
        null=True
    )
    about = models.TextField(default='no about yet')
    joined_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if not self.avatar:
            self.avatar = 'portal/default-avatar.png'
        
        if not self.banner:
            self.banner = 'portal/default-banner.png'
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.user.username}'s portal"
    