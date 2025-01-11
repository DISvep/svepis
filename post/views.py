from django.shortcuts import render
from django.views.generic import DetailView, ListView
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
    
    

