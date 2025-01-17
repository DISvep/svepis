from django.urls import path
from .views import ReactionView


urlpatterns = [
    path('post/<int:pk>', ReactionView.as_view(), name='post-reaction')
]
