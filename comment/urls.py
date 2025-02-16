from django.urls import path
from django.views.generic import TemplateView
from .views import PostCommentView, CreatePostCommentView, UpdatePostCommentView, DeletePostCommentView, CreateVideoCommentView, UpdateVideoCommentView, DeleteVideoCommentView


urlpatterns = [
    path('<int:pk>/', PostCommentView.as_view(), name='post-comments'),
    path('<int:pk>/create', CreatePostCommentView.as_view(), name='comment-create'),
    path('<int:pk>/update', UpdatePostCommentView.as_view(), name='comment-update'),
    path('<int:pk>/delete', DeletePostCommentView.as_view(), name='comment-delete'),
    path('<int:pk>/video-create', CreateVideoCommentView.as_view(), name='video-comment-create'),
    path('<int:pk>/video-update', UpdateVideoCommentView.as_view(), name='video-comment-update'),
    path('<int:pk>/video-delete', DeleteVideoCommentView.as_view(), name='video-comment-delete'),
]
