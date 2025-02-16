from django.contrib import admin
from .models import Chat, Message, PrivateChat, GroupChat


# Register your models here.
admin.site.register(Chat)
admin.site.register(PrivateChat)
admin.site.register(GroupChat)
admin.site.register(Message)
