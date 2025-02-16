from django.urls import path
from .views import ChatView, UserChatsList, UserSearchView, FriendSearchView, CreateOrGetChatView, CreateGroupChatView, EditGroupChatView, AddToGroupView, RemoveFromGroupGView


urlpatterns = [
    path('', UserChatsList.as_view(), name='chats'),
    path('<int:pk>/', ChatView.as_view(), name='chat-page'),
    path('get/<int:user_pk>/', CreateOrGetChatView.as_view(), name='get-chat'),
    path('search_users/', UserSearchView.as_view(), name='search-users'),
    path('search_friends/', FriendSearchView.as_view(), name='search-friends'),
    path('create_group/', CreateGroupChatView.as_view(), name='create-group'),
    path('edit_group/<int:pk>', EditGroupChatView.as_view(), name='edit-group'),
    path('add_to_group/', AddToGroupView.as_view(), name='add-to-group'),
    path('remove_from_group/', RemoveFromGroupGView.as_view(), name='remove-from-group')
]
