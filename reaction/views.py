from django.shortcuts import render
from post.models import Post
from .models import PostReaction
from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy


# Create your views here.
class ReactionView(LoginRequiredMixin, UpdateView):
    model = Post
    
    def post(self, request, *args, **kwargs):
        post_ = self.get_object()
        emoji = request.POST.get('emoji')
        
        if not emoji:
            return JsonResponse({'error': 'No emoji'}, status=400)
        
        reaction, created = PostReaction.objects.get_or_create(
            post=post_,
            emoji=emoji
        )
        
        if request.user in reaction.users.all():
            reaction.users.remove(request.user)
            if reaction.users.count() == 0:
                reaction.delete()
            return HttpResponseRedirect(reverse_lazy('post-list'))
        
        reaction.users.add(request.user)
        return HttpResponseRedirect(reverse_lazy('post-list'))
        