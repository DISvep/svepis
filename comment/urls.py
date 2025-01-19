from django.urls import path
from django.views.generic import TemplateView
from .views import PostCommentView, CreatePostCommentView, UpdatePostCommentView, DeletePostCommentView


urlpatterns = [
    path('<int:pk>/', PostCommentView.as_view(), name='post-comments'),
    path('<int:pk>/create', CreatePostCommentView.as_view(), name='comment-create'),
    path('<int:pk>/update', UpdatePostCommentView.as_view(), name='comment-update'),
    path('<int:pk>/delete', DeletePostCommentView.as_view(), name='comment-delete')
]
