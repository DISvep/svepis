from django.contrib.auth.models import User
from chat.models import Chat
from django.db import models


class MessageNotification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='message_notifications')
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def mark_as_read(self):
        self.is_read = True
        self.save()
    
    def __str__(self):
        return f"{self.user.username} - Message Notification - {'Read' if self.is_read else 'Unread'}"
