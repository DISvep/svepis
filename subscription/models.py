from django.db import models
from django.contrib.auth.models import User


class SubscriptionList(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='subscription_list')
    subscribers = models.ManyToManyField(User, blank=True, related_query_name='subscribers')
    subscriptions = models.ManyToManyField(User, blank=True, related_name="subscriptions")
    
    def __str__(self):
        return self.user.username
    
    def add_subscriber(self, account):
        if not account in self.subscribers.all():
            self.subscribers.add(account)
            
    def remove_subscriber(self, account):
        if account in self.subscribers.all():
            self.subscribers.remove(account)
    
    def subscribe(self, account):
        if not account in self.subscriptions.all():
            self.subscriptions.add(account)
            subscribers_account = SubscriptionList.objects.get(user=account)
            subscribers_account.add_subscriber(self.user)
    
    def unsubscribe(self, account):
        if account in self.subscriptions.all():
            self.subscriptions.remove(account)
            subscribers_account = SubscriptionList.objects.get(user=account)
            subscribers_account.remove_subscriber(self.user)


class FriendList(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="friend_list")
    friends = models.ManyToManyField(User, blank=True, related_name='friends')

    def __str__(self):
        return self.user.username

    def add_friend(self, account):
        if not account in self.friends.all():
            self.friends.add(account)
            
    def remove_friend(self, account):
        if account in self.friends.all():
            self.friends.remove(account)
    
    def unfriend(self, removee):
        remover_friends_list = self
        remover_friends_list.remove_friend(removee)
        friends_list = FriendList.objects.get(user=removee)
        friends_list.remove_friend(self.user)
    
    def is_mutual_friend(self, friend):
        if friend in self.friends.all():
            return True
        else:
            return False


class FriendRequest(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    is_active = models.BooleanField(blank=True, null=False, default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.sender.username} to {self.receiver.username}"
    
    def accept(self):
        receiver_friend_list = FriendList.objects.get(user=self.receiver)
        if receiver_friend_list:
            receiver_friend_list.add_friend(self.sender)
            sender_friend_list = FriendList.objects.get(user=self.sender)
            if sender_friend_list:
                sender_friend_list.add_friend(self.receiver)
                self.is_active = False
                self.delete()
    
    def decline(self):
        self.is_active = False
        self.delete()
    
    def cancel(self):
        self.is_active = False
        self.delete()
