from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CommentForm, VideoCommentForm
from .models import PostComment, VideoComment
from django.http import HttpResponseRedirect
from reaction.models import PostReaction
from django.db.models import Prefetch
from django.urls import reverse_lazy
from main.mixins import IsOwnerMixin
from django.shortcuts import render
from video.models import Video
from post.models import Post


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


class UpdatePostCommentView(LoginRequiredMixin, IsOwnerMixin, UpdateView):
    model = PostComment
    form_class = CommentForm
    
    def get_success_url(self):
        return reverse_lazy('post-comments', kwargs={'pk': self.object.post.pk})


class DeletePostCommentView(LoginRequiredMixin, IsOwnerMixin, DeleteView):
    model = PostComment
    
    def get_success_url(self):
        return reverse_lazy('post-comments', kwargs={'pk': self.object.post.pk})


class CreateVideoCommentView(LoginRequiredMixin, CreateView):
    model = VideoComment

    def post(self, request, *args, **kwargs):
        form = VideoCommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.video = Video.objects.get(pk=request.POST.get('post_pk'))
            comment.save()

            return HttpResponseRedirect(reverse_lazy('video', kwargs={'pk': request.POST.get('post_pk')}))
        else:
            return HttpResponseRedirect(reverse_lazy('video', kwargs={'pk': request.POST.get('post_pk')}))


class UpdateVideoCommentView(LoginRequiredMixin, IsOwnerMixin, UpdateView):
    model = VideoComment
    form_class = VideoCommentForm

    def get_success_url(self):
        return reverse_lazy('video', kwargs={'pk': self.object.video.pk})


class DeleteVideoCommentView(LoginRequiredMixin, IsOwnerMixin, DeleteView):
    model = VideoComment

    def get_success_url(self):
        return reverse_lazy('video', kwargs={'pk': self.object.video.pk})
    