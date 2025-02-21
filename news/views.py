from subscription.models import FriendList, SubscriptionList
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.views.generic import ListView
from reaction.models import PostReaction
from django.db.models import Prefetch
from post.models import Post
import random


# Create your views here.
class DiscoveryView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'discovery.html'
    context_object_name = 'posts'
    
    def get_queryset(self):
        user = self.request.user
        
        friend_list = get_object_or_404(FriendList, user=user)
        subscription_list = get_object_or_404(SubscriptionList, user=user)
        
        friends = friend_list.friends.all()
        subscriptions = subscription_list.subscriptions.all()

        reactions_prefetch = Prefetch(
            'reactions', queryset=PostReaction.objects.prefetch_related('users')
        )
        
        return Post.objects.filter(user__in=friends | subscriptions).prefetch_related(reactions_prefetch).select_related('user')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts = context['posts']
        
        posts_with_reactions = {
            post: {reaction.emoji: reaction.users.count() for reaction in post.reactions.all()}
            for post in posts
        }
        
        context['PostReactions'] = posts_with_reactions
        
        friend_list = get_object_or_404(FriendList, user=self.request.user)
        friends = set(friend_list.friends.all())
        
        mutual_friends = set()
        for friend in friends:
            friend_friend_list = get_object_or_404(FriendList, user=friend)
            friend_friends = friend_friend_list.friends.all()
            mutual_friends.update(friend_friends)
        
        mutual_friends -= friends
        mutual_friends.discard(self.request.user)
    
        all_users = set(User.objects.exclude(id=self.request.user.id))
        potential_friends = all_users - mutual_friends
        potential_friends = list(potential_friends - friends)
        random.shuffle(potential_friends)
        
        suggested_users = list(mutual_friends)[:5] + potential_friends[:5]
        context['SuggestedUsers'] = suggested_users
        
        return context
        