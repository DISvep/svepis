from django.db.models.signals import post_save
from .models import MessageNotification
from django.dispatch import receiver
from chat.models import Message


@receiver(post_save, sender=Message)
def message_notification(sender, instance, created, **kwargs):
    if created:
        chat = instance.room
        sender = instance.sender
        members = chat.members.exclude(pk=sender.pk)
        
        for user in members:
            MessageNotification.objects.create(
                user=user,
                chat=chat,
            )
            