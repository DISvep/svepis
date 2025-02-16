from subscription.models import FriendList, SubscriptionList
from django.contrib.auth.models import User
from portal.models import Portal
import os

username = os.getenv("DJANGO_SUPERUSER_USERNAME")
email = os.getenv("DJANGO_SUPERUSER_EMAIL")
password = os.getenv("DJANGO_SUPERUSER_PASSWORD")

if not User.objects.filter(username=username).exists():
    superuser = User.objects.create_superuser(username=username, email=email, password=password)
    
    Portal.objects.create(user=superuser)
    FriendList.objects.create(user=superuser)
    SubscriptionList.objects.create(user=superuser)
    
    superuser.portal.save()
    
    print("Superuser created")
else:
    print("Superuser already exists")
