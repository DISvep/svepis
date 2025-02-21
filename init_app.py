import os
import base64
import json
import subprocess
from main.drive_service import download_file
from django.core.management import call_command
import django

# Декодируем ключ Google Drive
print("Decoding Google Drive key...")
gdrive_key_b64 = os.getenv("GDRIVE_KEY")
if gdrive_key_b64:
    gdrive_key_json = base64.b64decode(gdrive_key_b64).decode("utf-8")
    with open("/app/gdrive_key.json", "w") as key_file:
        key_file.write(gdrive_key_json)
    print("Google Drive key saved.")
else:
    print("Warning: GDRIVE_KEY is missing!")
    
    
django.setup()

print("Applying migrations...")
call_command("migrate", "--noinput")

# Загружаем базу данных
print("Downloading database from Google Drive...")
download_file("backup.json", "db_backup.json")

if os.path.exists("db_backup.json"):
    os.system('python manage.py loaddata db_backup.json')
    print('Database restored from backup!')

# Загружаем и распаковываем медиафайлы
print("Downloading media files from Google Drive...")

download_file("media_backup.zip", "media_backup.zip")

if os.path.exists('media_backup.zip'):
    os.system('unzip -o media_backup.zip')
    
    print('Media files restored!')
    
    for root, dirs, files in os.walk('media'):
        print(root, dirst, files)
        for file in files:
            print(os.path.join(root, file))


# Применяем миграции и собираем статику
print("Collecting static files...")
call_command("collectstatic", "--noinput")

# Создаем суперпользователя
print("Creating superuser...")
subprocess.run(["python", "manage.py", "shell", "-c", "exec(open('/app/create_superuser.py').read())"], check=True)
print("Initialization complete.")
