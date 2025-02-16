from .views import MainView, VideoView, LikeView, DislikeView
from django.urls import path


urlpatterns = [
    path('', MainView.as_view(), name='main-video'),
    path('<int:pk>/', VideoView.as_view(), name='video'),
    path('<int:pk>/like/', LikeView.as_view(), name='like-video'),
    path('<int:pk>/dislike/', DislikeView.as_view(), name='dislike-video'),
]
