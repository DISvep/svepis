from django.core.management import call_command
from .drive_service import upload_file
import atexit
import os


DB_BACKUP_PATH = 'db_backup.json'
GDRIVE_FILENAME = "backup.json"
MEDIA_FOLDER = 'media'
GDRIVE_MEDIA_FOLDER = 'media_backup.zip'


def backup_db():
    print('Backing up database before shutdown...')
    
    call_command('dumpdata', output=DB_BACKUP_PATH)
    upload_file(BD_BACKUP_PATH, GDRIVE_FILENAME)
    
    print(f"Database backup {GDRIVE_FILENAME} uploaded to Google Drive.")

    print('Backing up media files before shutdown...')
    
    os.system(f"zip -r {GDRIVE_MEDIA_FOLDER} {MEDIA_FOLDER}")
    upload_file(GDRIVE_MEDIA_FOLDER, GDRIVE_MEDIA_FOLDER)
    
    print(f'Media files backup {GDRIVE_MEDIA_FOLDER} uploaded to Google Drive.')


atexit.register(backup_db)
