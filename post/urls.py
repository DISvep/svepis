from django.urls import path
from .views import PostList, PostDetail, CreatePost


urlpatterns = [
    path('', PostList.as_view(), name='post-list'),
    path('create/', CreatePost.as_view(), name='create-post'),
    path('<int:pk>/', PostDetail.as_view(), name='post'),
]