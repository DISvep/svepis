from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from .serializers import PostSerializer, AnnouncementSerializer
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect
from reaction.models import PostReaction
from django.db.models import Prefetch
from django.urls import reverse_lazy
from main.mixins import IsOwnerMixin
from rest_framework import generics
from .forms import PostForm
from .models import Post


# Create your views here.
class PostDetail(DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'


class PostList(ListView):
    model = Post
    template_name = 'post_list.html'
    context_object_name = 'posts'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['PostForm'] = PostForm
        
        posts = Post.objects.prefetch_related(
            Prefetch('reactions', queryset=PostReaction.objects.prefetch_related('users'))
        ).order_by('-date')
        posts_with_reactions = {
            post: {reaction.emoji: reaction.count() for reaction in post.reactions.all()}
            for post in posts
        }
        context['PostReactions'] = posts_with_reactions
        
        return context
    
    def get_queryset(self):
        return Post.objects.all().order_by('-date')
    

class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    
    def post(self, request, *args, **kwargs):
        form = PostForm(request.POST)
        
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            
            return HttpResponseRedirect(reverse('post-list'))
        else:
            return HttpResponseRedirect(reverse('post-list'))


class PostUpdate(LoginRequiredMixin, IsOwnerMixin, UpdateView):
    model = Post
    form_class = PostForm
        
    def get_success_url(self):
        return reverse_lazy('post-list')


class PostDelete(LoginRequiredMixin, IsOwnerMixin, DeleteView):
    model = Post
    
    def get_success_url(self):
        return reverse_lazy('post-list')


class PostListAPI(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
