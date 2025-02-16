from django.contrib import admin
from .models import FriendList, FriendRequest, SubscriptionList


# Register your models here.
admin.site.register(FriendList)
admin.site.register(FriendRequest)
admin.site.register(SubscriptionList)
