from django.core.management.base import BaseCommand
from main.drive_service import download_file
import os


class Command(BaseCommand):
    def handle(self, *args, **options):
        GDRIVE_MEDIA_FOLDER = 'media_backup.zip'
        LOCAL_MEDIA_FOLDER = "media_backup.zip"
        
        print('Downloading latest media files backup...')
        download_file(GDRIVE_MEDIA_FOLDER, LOCAL_MEDIA_FOLDER)
        
        if os.path.exists(LOCAL_MEDIA_FOLDER):
            print('Extracting media files...')
            
            os.system(f'unzip -o {LOCAL_MEDIA_FOLDER} -d media/')
            
            if os.path.exists('media/media'):
                os.system('mv media/media/* media/ && rmdir media/media')
            
            print("Media files restored successfully.")

            print("Checking extracted media files...")
            os.system("ls -R media")
        