from django.shortcuts import render
from django.views.generic import DetailView, UpdateView
from .models import Portal
from .forms import PortalForm
from django.db.models.signals import post_save
from django.db.models import Prefetch
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from widget.models import Widget


class PortalDetail(DetailView):
    model = Portal
    template_name = 'portal_detail.html'
    context_object_name = 'portal'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['widgets'] = self.object.user.widgets.all()
        
        return context


class PortalCreate(UpdateView):
    model = Portal
    form_class = PortalForm
    template_name = 'portal_create.html'
    
    def get_success_url(self):
        return reverse_lazy('portal', kwargs={'pk': self.object.pk})
    
    def get_object(self, queryset=None):
        return self.request.user.portal


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Portal.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.portal.save()
    