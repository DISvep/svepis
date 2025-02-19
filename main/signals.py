from django.core.management import call_command
from .drive_service import upload_file
from django.conf import settings
import atexit
import os


def backup_db():
    print('Backing up database before shutdown...')
    
    call_command('dumpdata', output=settings.DB_BACKUP_PATH)
    upload_file(settings.BD_BACKUP_PATH, settings.GDRIVE_FILENAME)
    
    print(f"Database backup {settings.GDRIVE_FILENAME} uploaded to Google Drive.")

    print('Backing up media files before shutdown...')
    
    os.system(f"zip -r {settings.GDRIVE_MEDIA_FOLDER} {settings.MEDIA_FOLDER}")
    upload_file(settings.GDRIVE_MEDIA_FOLDER, settings.GDRIVE_MEDIA_FOLDER)
    
    print(f'Media files backup {settings.GDRIVE_MEDIA_FOLDER} uploaded to Google Drive.')


atexit.register(backup_db)
