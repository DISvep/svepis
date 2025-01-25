from django.db import models
from django.contrib.auth.models import User


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
