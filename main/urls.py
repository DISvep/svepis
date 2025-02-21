from .views import CustomLoginView, CustomRegistrationView, IndexView, load_more_announcements, GoogleDriveView
from django.contrib.auth.views import LogoutView
from django.urls import path


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', CustomRegistrationView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('load-more-announcements/', load_more_announcements, name='load-more-announcements'),
    path('gdrive/', GoogleDriveView.as_view(), name='gdrive_home'),
]