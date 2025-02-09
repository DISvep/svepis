from django.urls import path
from .views import DiscoveryView


urlpatterns = [
    path('', DiscoveryView.as_view(), name='discovery')
]