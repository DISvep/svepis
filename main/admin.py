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


# Register your models here.
class GoogleDriveAdmin(admin.ModelAdmin):
    change_list_template = 'admin/gdrive_change_list.html'
    
    def get_urls(self):
        urls = super().get_urls()
        
        custom_urls = [
            path('backup/', self.admin_site.admin_view(self.backup_view), name='gdrive-backup'),
            path('list/', self.admin_site.admin_view(self.list_view), name='gdrive-list'),
            path('delete/<str:file_id>/', self.admin_site.admin_view(self.delete_view), name='gdrive-delete'),
        ]
        return custom_urls + urls
    
    def backup_view(self, request):
        try:
            call_command('dumpdata', output=DB_BACKUP_PATH)
            upload_file(DB_BACKUP_PATH, GDRIVE_FILENAME)
            
            os.system(f'zip -r {GDRIVE_MEDIA_FOLDER} {MEDIA_FOLDER}')
            upload_file(GDRIVE_MEDIA_FOLDER, GDRIVE_FILENAME)
            
            self.message_user(request, 'Backup of db and media is successfully uploaded to Google Drive', messages.SUCCESS)
        except Exception as e:
            self.message_user(request, f"Error while backup data! {e}", messages.ERROR)
        return HttpResponseRedirect(reverse('admin:gdrive-list'))

    def list_view(self, request):
        drive = get_drive()
        
        file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
        context = dict(
            self.admin_site.each_context(request),
            files=file_list,
        )
        return TemplateResponse(request, 'admin/gdrive_list.html', context)
    
    def delete_view(self, request, file_id):
        try:
            delete_file(file_id)
            self.message_user(request, 'File successfully deleted', messages.SUCCESS)
        except Exception as e:
            self.message_user(request, f"Error while deleting file! {e}", messages.ERROR)
        return HttpResponseRedirect(reverse('admin:gdrive-list'))


from django.contrib.auth.models import User

admin.site.register(User, GoogleDriveAdmin)
