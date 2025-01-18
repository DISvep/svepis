from django.shortcuts import render
from django.views.generic import DetailView, CreateView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from .models import PostComment
from .forms import CommentForm
from post.models import Post
from reaction.models import PostReaction
from django.db.models import Prefetch
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.
class PostCommentView(DetailView):
    model = Post
    template_name = 'comment_list.html'
    context_object_name = 'post'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['comment_form'] = CommentForm
        
        reactions = PostReaction.objects.filter(post=self.object).prefetch_related('users')
        reactions_dict = {reaction.emoji: reaction.count() for reaction in reactions}
        
        context['reactions'] = reactions_dict
        
        return context


class CreatePostCommentView(LoginRequiredMixin, CreateView):
    model = PostComment
    
    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = Post.objects.get(pk=request.POST.get('post_pk'))
            comment.save()
            
            return HttpResponseRedirect(reverse_lazy('post-comments', kwargs={'pk': request.POST.get('post_pk')}))
        else:
            return HttpResponseRedirect(reverse_lazy('post-comments', kwargs={'pk': request.POST.get('post_pk')}))
