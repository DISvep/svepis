from .drive_service import get_drive, delete_file, upload_file
from django.template.response import TemplateResponse
from django.core.management import call_command
from django.http import HttpResponseRedirect
from django.urls import path, reverse
from django.contrib import messages
from django.contrib import admin
import os


DB_BACKUP_PATH = 'db_backup.json'
GDRIVE_FILENAME = "backup.json"
MEDIA_FOLDER = 'media'
GDRIVE_MEDIA_FOLDER = 'media_backup.zip'

    
def gdrive_list_view(self, request):
    drive = get_drive()
    
    file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
    context = {
        **admin.site.each_context(request),
        'files': file_list,
        'title': 'Google Drive Files',
    }
    return TemplateResponse(request, 'admin/gdrive_list.html', context)


def gdrive_backup_view(self, request):
    try:
        call_command('dumpdata', output=DB_BACKUP_PATH)
        upload_file(DB_BACKUP_PATH, GDRIVE_FILENAME)
        
        os.system(f'zip -r {GDRIVE_MEDIA_FOLDER} {MEDIA_FOLDER}')
        upload_file(GDRIVE_MEDIA_FOLDER, GDRIVE_FILENAME)
        
        messages.success(request, 'Backup of db and media is successfully uploaded to Google Drive')
    except Exception as e:
        messages.error(request, f"Error while backup data! {e}")
    return HttpResponseRedirect(reverse('admin:gdrive-list'))


def gdrive_delete_view(self, request, file_id):
    try:
        delete_file(file_id)
        messages.success(request, 'File successfully deleted')
    except Exception as e:
        nessages.error(request, f"Error while deleting file! {e}")
    return HttpResponseRedirect(reverse('admin:gdrive-list'))


class GoogleDriveAdminSite(admin.AdminSite):
    def get_urls(self):
        urls = super().get_urls()
        
        custom_urls = [
            path('gdrive/list/', self.admin_view(gdrive_list_view), name='gdrive-list'),
            path('gdrive/backup/', self.admin_view(gdrive_backup_view), name='gdrive-backup'),
            path('gdrive/delete/<str:file_id>/', self.admin_view(gdrive_delete_view), name='gdrive-delete'),
        ]
        
        return custom_urls + urls


admin.site = GoogleDriveAdminSite()


from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

admin.site.register(User, UserAdmin)
