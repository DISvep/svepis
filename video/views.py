from django.views.generic import ListView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from comment.forms import VideoCommentForm
from django.urls import reverse_lazy
from django.shortcuts import render
from .models import Video


# Create your views here.
class MainView(ListView):
    model = Video
    template_name = 'main_page.html'
    context_object_name = 'videos'


class VideoView(DetailView):
    model = Video
    template_name = 'video_page.html'
    context_object_name = 'video'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['comment_form'] = VideoCommentForm
        
        return context


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
        