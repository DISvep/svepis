from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from .models import Post
from .forms import PostForm
from main.mixins import IsOwnerMixin


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
        
        return context
    
    def get_queryset(self):
        return Post.objects.all().order_by('-date')
    

class PostCreate(CreateView):
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


class PostUpdate(IsOwnerMixin, UpdateView):
    model = Post
    form_class = PostForm
        
    def get_success_url(self):
        return reverse_lazy('post-list')


class PostDelete(IsOwnerMixin, DeleteView):
    model = Post
    
    def get_success_url(self):
        return reverse_lazy('post-list')
    
