from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from .models import FriendRequest


# Create your views here.
class SubscribeButtonView(LoginRequiredMixin, View):
    def post(self, request, user_pk, *args, **kwargs):
        portal = get_object_or_404(User, pk=user_pk)
        
        if portal != request.user:
            if portal in request.user.subscription_list.subscriptions.all():
                request.user.subscription_list.unsubscribe(portal)
            else:
                request.user.subscription_list.subscribe(portal)
        
        next_url = request.GET.get('next')
        
        if not next_url:
            return HttpResponseRedirect(reverse_lazy('portal', kwargs={'pk': portal.portal.pk}))
        
        return HttpResponseRedirect(next_url)


class SendFriendRequestView(LoginRequiredMixin, View):
    def post(self, request, user_pk, *args, **kwargs):
        receiver = get_object_or_404(User, pk=user_pk)
        
        if receiver != request.user:
            existing_request = FriendRequest.objects.filter(
                sender=request.user, receiver=receiver, is_active=True
            ).first()
            if not existing_request:
                FriendRequest.objects.create(sender=request.user, receiver=receiver)
            else:
                existing_request.cancel()
        return HttpResponseRedirect(reverse_lazy('portal', kwargs={'pk': receiver.portal.pk}))


class DeleteFriendView(LoginRequiredMixin, View):
    def post(self, request, user_pk, *args, **kwargs):
        receiver = get_object_or_404(User, pk=user_pk)
        
        if receiver != request.user:
            request.user.friend_list.unfriend(receiver)
        
        return HttpResponseRedirect(reverse_lazy('portal', kwargs={'pk': receiver.portal.pk}))


class AcceptRequestView(LoginRequiredMixin, View):
    def post(self, request, user_pk, *args, **kwargs):
        sender = get_object_or_404(User, pk=user_pk)
        if sender != request.user:
            existing_request = FriendRequest.objects.filter(
                sender=sender, receiver=request.user, is_active=True
            ).first()
            if existing_request:
                existing_request.accept()
        return HttpResponseRedirect(reverse_lazy('portal', kwargs={'pk': sender.portal.pk}))


class CancelRequestView(LoginRequiredMixin, View):
    def post(self, request, user_pk, *args, **kwargs):
        sender = get_object_or_404(User, pk=user_pk)
        if sender != request.user:
            existing_request = FriendRequest.objects.filter(
                sender=sender, receiver=request.user, is_active=True
            ).first()
            if existing_request:
                existing_request.cancel()
        return HttpResponseRedirect(reverse_lazy('portal', kwargs={'pk': sender.portal.pk}))

