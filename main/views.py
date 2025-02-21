from django.contrib.admin.views.decorators import staff_member_required
from .drive_service import get_drive, upload_file, delete_file
from .forms import CustomRegistrationForm, CustomLoginForm
from django.views.generic import CreateView, TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.views import LoginView
from django.core.management import call_command
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib import messages
from django.urls import reverse
import post.models
import os


DB_BACKUP_PATH = 'db_backup.json'
GDRIVE_FILENAME = "backup.json"
MEDIA_FOLDER = 'media'
GDRIVE_MEDIA_FOLDER = 'media_backup.zip'


# Create your views here.
@method_decorator(staff_member_required, name='dispatch')
class GoogleDriveView(TemplateView):
    template_name = 'gdrive_home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        drive = get_drive()
        file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
        context['files'] = file_list
        
        return context
    
    def post(self, request, *args, **kwargs):
        if 'backup' in request.POST:
            try:
                call_command('dumpdata', output=DB_BACKUP_PATH)
                upload_file(DB_BACKUP_PATH, GDRIVE_FILENAME)
                
                os.system(f"zip -r {GDRIVE_MEDIA_FOLDER} {MEDIA_FOLDER}")
                upload_file(GDRIVE_MEDIA_FOLDER, GDRIVE_MEDIA_FOLDER)
                
                messages.success(request, "Backup successfully created and uploaded to Google Drive")
            except Exception as e:
                messages.error(request, f"Error backup: {e}")
        elif 'delete' in request.POST:
            file_id = request.POST.get('file_id')
            if file_id:
                try:
                    delete_file(file_id)
                    messages.success(request, "File successfully deleted from Google Drive")
                except Exception as e:
                    messages.error(request, f"Error deleting: {e}")
        return redirect('gdrive-home')
                

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
        