from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView, TemplateView
from django.contrib.auth.models import User
from .forms import CustomRegistrationForm, CustomLoginForm
import post.models


# Create your views here.
class IndexView(TemplateView):
    template_name = 'index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Announcements'] = post.models.Announcement.objects.all()
        
        return context


def load_more_announcements(request):
    offset = int(request.GET.get('offset', 0))
    limit = 1
    announcements = post.models.Announcement.objects.all()[offset:offset + limit]
    data = [
        {'pk': a.pk} for a in announcements
    ]
    return JsonResponse({'announcements': data})


class CustomRegistrationView(CreateView):
    model = User
    form_class = CustomRegistrationForm
    template_name = 'register.html'
    success_url = '/login/'
    
    def form_valid(self, form):
        response = super().form_valid(form)
        self.request.session['success_message'] = "Thank you for the registration!"
        
        return response


class CustomLoginView(LoginView):
    template_name = 'login.html'
    form_class = CustomLoginForm
    success_url = '/'
        