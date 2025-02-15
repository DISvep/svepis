from django.views.generic import ListView, View, CreateView, UpdateView, DetailView
from django.shortcuts import get_object_or_404, redirect, reverse
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import GroupChatForm, EditGroupChatForm
from .models import Chat, PrivateChat, GroupChat
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from .mixins import IsChatMember
import json


# Create your views here.
class ChatView(LoginRequiredMixin, IsChatMember, DetailView):
    model = Chat
    template_name = 'chat.html'
    context_object_name = 'room'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['messages'] = self.object.messages.all()

        context['currentChatName'] = self.object.get_title(current_user=self.request.user)

        get_chats = Chat.objects.all().filter(members=self.request.user)
        chats = {chat.get_title(current_user=self.request.user): [chat.get_avatar(current_user=self.request.user),
                                                                  chat.get_last_message, chat.pk] for chat in get_chats}
        context['chats'] = chats

        context['groupForm'] = GroupChatForm
        context['editGroupForm'] = EditGroupChatForm

        return context


class CreateOrGetChatView(LoginRequiredMixin, View):
    def get(self, request, user_pk):
        user1 = request.user
        user2 = get_object_or_404(User, pk=user_pk)

        if user1 == user2:
            return redirect('portal', pk=user1.portal.pk)

        chat, _ = PrivateChat.get_or_create_private_chat(user1, user2)
        return redirect('chat-page', pk=chat.pk)


class CreateGroupChatView(LoginRequiredMixin, CreateView):
    model = GroupChat
    form_class = GroupChatForm

    def form_valid(self, form):
        form.instance.private = False
        form.instance.user = self.request.user
        form.save()
        form.instance.members.add(self.request.user)

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('chat-page', kwargs={'pk': self.object.pk})


class EditGroupChatView(LoginRequiredMixin, UpdateView):
    model = GroupChat
    form_class = EditGroupChatForm

    def get_success_url(self):
        return reverse_lazy('chat-page', kwargs={'pk': self.object.pk})


class AddToGroupView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        user_id = data.get('user_id')
        group_id = data.get('group_id')

        group = get_object_or_404(GroupChat, id=group_id)
        user = get_object_or_404(User, id=user_id)

        if user not in group.members.all() and user in request.user.friend_list.friends.all():
            group.members.add(user)


class RemoveFromGroupGView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        user_id = data.get('user_id')
        group_id = data.get('group_id')

        group = get_object_or_404(GroupChat, id=group_id)
        user = get_object_or_404(User, id=user_id)

        if user in group.members.all():
            group.members.remove(user)


class UserChatsList(LoginRequiredMixin, ListView):
    models = Chat
    template_name = 'chats_page.html'

    def get_queryset(self):
        return Chat.objects.filter(members=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        chats = {
            chat.get_title(
                current_user=self.request.user
            ): [
                chat.get_avatar(current_user=self.request.user),
                chat.get_last_message,
                chat.pk
            ]
            for chat in self.get_queryset()
        }
        context['chats'] = chats

        context['groupForm'] = GroupChatForm

        return context


class UserSearchView(View):
    def get(self, request, *args, **kwargs):
        query = request.GET.get('q', '')
        if query:
            users = User.objects.filter(username__icontains=query).exclude(pk=request.user.pk)[:10]
            results = [{'pk': user.pk, 'username': user.username} for user in users]

            return JsonResponse({'users': results})
        return JsonResponse({'users': []})


class FriendSearchView(View):
    def get(self, request, *args, **kwargs):
        query = request.GET.get('q', '')
        group_id = request.GET.get('group_id')

        if query:
            group = get_object_or_404(GroupChat, id=group_id)
            users = request.user.friend_list.friends.exclude(id__in=group.members.values_list('id', flat=True)) \
                        .filter(username__icontains=query)[:10]
            results = [{'pk': user.pk, 'username': user.username} for user in users]

            return JsonResponse({'users': results})
        return JsonResponse({'users': []})
