from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect
from django.views.generic import DetailView, ListView, CreateView
from .models import Post
from .forms import PostForm


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
    

class CreatePost(CreateView):
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

