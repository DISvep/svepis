from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse
from comment.forms import VideoCommentForm
from django.urls import reverse_lazy
from .forms import VideoForm
from .models import Video


# Create your views here.
class MainView(ListView):
    model = Video
    template_name = 'main_page.html'
    context_object_name = 'videos'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['VideoForm'] = VideoForm
        
        return context


class VideoView(DetailView):
    model = Video
    template_name = 'video_page.html'
    context_object_name = 'video'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['comment_form'] = VideoCommentForm
        
        return context


class VideoCreateView(LoginRequiredMixin, CreateView):
    model = Video
    
    def post(self, request, *args, **kwargs):
        form = VideoForm(request.POST, request.FILES)
        
        print('video form')
        
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            
            return HttpResponseRedirect(reverse('main-video'))
        else:
            return HttpResponseRedirect(reverse('main-video'))
        
        
class VideoDeleteView(LoginRequiredMixin, DeleteView):
    model = Video
    success_url = '/video'


class LikeView(LoginRequiredMixin, UpdateView):
    model = Video

    def post(self, request, *args, **kwargs):
        video = self.get_object()

        if video.dislikes.filter(id=request.user.id).exists():
            video.dislikes.remove(request.user)

        if video.likes.filter(id=request.user.id).exists():
            video.likes.remove(request.user)
        else:
            video.likes.add(request.user)

        return HttpResponseRedirect(reverse_lazy('video', kwargs={'pk': video.pk}))


class DislikeView(LoginRequiredMixin, UpdateView):
    model = Video

    def post(self, request, *args, **kwargs):
        video = self.get_object()

        if video.likes.filter(id=request.user.id).exists():
            video.likes.remove(request.user)

        if video.dislikes.filter(id=request.user.id).exists():
            video.dislikes.remove(request.user)
        else:
            video.dislikes.add(request.user)

        return HttpResponseRedirect(reverse_lazy('video', kwargs={'pk': video.pk}))
        