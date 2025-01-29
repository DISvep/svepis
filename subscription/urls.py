from django.urls import path
from .views import SendFriendRequestView, AcceptRequestView, CancelRequestView, DeleteFriendView


urlpatterns = [
    path('send-request/<int:user_pk>/', SendFriendRequestView.as_view(), name='send-request'),
    path('accept/<int:user_pk>/', AcceptRequestView.as_view(), name='accept'),
    path('cancel/<int:user_pk>/', CancelRequestView.as_view(), name='cancel'),
    path('delete/<int:user_pk>/', DeleteFriendView.as_view(), name='delete-friend')
]
