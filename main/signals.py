# from django.core.management import call_command
# from .drive_service import upload_file
# import atexit
# import os
# 
# 
# DB_BACKUP_PATH = 'db_backup.json'
# GDRIVE_FILENAME = "backup.json"
# MEDIA_FOLDER = 'media'
# GDRIVE_MEDIA_FOLDER = 'media_backup.zip'
# 
# 
# def backup_db():
#     print('Backing up database before shutdown...')
# 
#     call_command('dumpdata', output=DB_BACKUP_PATH)
#     upload_file(DB_BACKUP_PATH, GDRIVE_FILENAME)
# 
#     print(f"Database backup {GDRIVE_FILENAME} uploaded to Google Drive.")
# 
#     print('Backing up media files before shutdown...')
# 
#     media_files = os.listdir(os.path.join(MEDIA_FOLDER, 'portal')) if os.path.isdir(MEDIA_FOLDER) else []
# 
#     if media_files and not len(media_files) == 3:
#         os.system(f"zip -r {GDRIVE_MEDIA_FOLDER} {MEDIA_FOLDER}")
#         upload_file(GDRIVE_MEDIA_FOLDER, GDRIVE_MEDIA_FOLDER)
# 
#         print(f'Media files backup {GDRIVE_MEDIA_FOLDER} uploaded to Google Drive.')
#     else:
#         print("Media folder is empty or contains only default values; skipping media backup.")
# 
# 
# atexit.register(backup_db)
