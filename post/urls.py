from django.urls import path
from .views import PostList, PostCreate, PostUpdate, PostDelete, PostListAPI


urlpatterns = [
    path('', PostList.as_view(), name='post-list'),
    path('create/', PostCreate.as_view(), name='post-create'),
    path('update/<int:pk>', PostUpdate.as_view(), name='post-update'),
    path('delete/<int:pk>', PostDelete.as_view(), name='post-delete'),
    path('api/posts/', PostListAPI.as_view(), name='post-list-api')
]