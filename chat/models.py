from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


# Create your models here.
class Chat(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    avatar = models.ImageField(upload_to='chat/avatar/', blank=True, null=True)
    members = models.ManyToManyField(User,  related_name="chats")
    private = models.BooleanField(default=True)

    def get_title(self, current_user=None):
        if self.name:
            return self.name

        qs = self.members.all()
        if current_user is None:
            return ', '.join(user.username for user in self.members.all()[:3]) + '...'
        else:
            qs = qs.exclude(pk=current_user.pk)

        other = qs.first()
        if other:
            return other.username
    
    def get_avatar(self, current_user=None):
        if self.avatar:
            return self.avatar.url
        
        qs = self.members.all()
        if current_user is not None:
            qs = qs.exclude(pk=current_user.pk)
        
        other = qs.first()
        if other:
            return other.portal.avatar.url
        
        return "/media/portal/default-avatar.png" if self.private else "/media/portal/default-group.png"
    
    def get_last_message(self):
        message = Message.objects.filter(room=self).latest('date')
        return ' '.join(('[image]' if message.have_image() else '', message.content if message.content else ''))

    def __str__(self):
        return self.get_title()


class PrivateChat(Chat):
    class Meta:
        verbose_name = "Private chat"
        verbose_name_plural = "Private chats"
    
    def clean(self):
        if self.pk and self.members.count() != 2:
            raise ValidationError("In private chats there is only 2 users!")
    
    @classmethod
    def get_or_create_private_chat(cls, user1, user2):
        users = sorted([user1, user2], key=lambda u: u.pk)
        
        qs = cls.objects.filter(members__pk=users[0].pk).filter(members__pk=users[1].pk)
        
        for chat in qs:
            if chat.members.count() == 2:
                return chat, False
      
        chat = cls.objects.create()
        chat.members.add(*users)
        chat.clean()
        
        return chat, True
    
    def __str__(self):
        return self.name or ", ".join(user.username for user in self.members.all())


class GroupChat(Chat):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_groups')
    
    class Meta:
        verbose_name = "Group chat"
        verbose_name_plural = "Group chats"
    
    def __str__(self):
        return self.name or ', '.join(user.username for user in self.members.all())


class Message(models.Model):
    room = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True)
    image = models.ImageField(
        upload_to='chat/message_images/',
        blank=True,
        null=True,
    )
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.content[:30]}"
    
    def have_image(self):
        have = True if self.image else False
        return True if self.image else False
