from django.urls import path
from .views import PortalDetail, PortalCreate


urlpatterns = [
    path('<int:pk>/', PortalDetail.as_view(), name='portal'),
    path('create/', PortalCreate.as_view(), name='portal-create')
]