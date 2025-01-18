from django.urls import path
from django.views.generic import TemplateView
from .views import PostCommentView, CreatePostCommentView


urlpatterns = [
    path('<int:pk>/', PostCommentView.as_view(), name='post-comments'),
    path('<int:pk>/create', CreatePostCommentView.as_view(), name='comment-create')
]
