from django.core.management.base import BaseCommand
from main.drive_service import download_file
import os


class Command(BaseCommand):
    def handle(self, *args, **options):
        LOCAL_PATH = 'db_backup.json'
        GDRIVE_FILENAME = 'backup.json'
        
        print('Downloading latest database backup...')
        download_file(GDRIVE_FILENAME, LOCAL_PATH)
        
        if os.path.exists(LOCAL_PATH):
            print("Restoring database...")
            os.system(f"python manage.py loaddata {LOCAL_PATH}")
            print('Database restored successfully')
