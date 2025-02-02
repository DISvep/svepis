from django.urls import path
from .views import ChatView, UserChatsList, UserSearchView, CreateOrGetChatView


urlpatterns = [
    path('', UserChatsList.as_view(), name='chats'),
    path('<int:pk>/', ChatView.as_view(), name='chat-page'),
    path('get/<int:user_pk>/',CreateOrGetChatView.as_view(), name='get-chat'),
    path('search_users/', UserSearchView.as_view(), name='search-users'),
]