from django.views.generic import DetailView, ListView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.models import User
from .models import Chat, PrivateChat
from django.http import JsonResponse


# Create your views here.
class ChatView(LoginRequiredMixin, DetailView):
    model = Chat
    template_name = 'chat.html'
    context_object_name = 'room'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['messages'] = self.object.messages.all()
        context['receiver'] = self.object.get_title(current_user=self.request.user)
        context['chats'] = Chat.objects.all().filter(members=self.request.user)

        return context


class CreateOrGetChatView(LoginRequiredMixin, View):
    def get(self, request, user_pk):
        user1 = request.user
        user2 = get_object_or_404(User, pk=user_pk)
        
        if user1 == user2:
            return redirect('portal', pk=user1.portal.pk)
        
        chat, _ = PrivateChat.get_or_create_private_chat(user1, user2)
        return redirect('chat-page', pk=chat.pk)


class UserChatsList(LoginRequiredMixin, ListView):
    models = Chat
    template_name = 'chats_page.html'
    context_object_name = 'chats'
    
    def get_queryset(self):
        return Chat.objects.filter(members=self.request.user)


class UserSearchView(View):
    def get(self, request, *args, **kwargs):
        query = request.GET.get('q', '')
        if query:
            users = User.objects.filter(username__icontains=query).exclude(pk=request.user.pk)[:10]
            results = [{'pk': user.pk, 'username': user.username} for user in users]
            
            return JsonResponse({'users': results})
        return JsonResponse({'users': []})
