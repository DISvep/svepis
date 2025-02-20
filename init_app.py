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

# Загружаем базу данных
print("Downloading database from Google Drive...")
download_file("db.sqlite3", "db.sqlite3")

# Загружаем и распаковываем медиафайлы
print("Downloading media files from Google Drive...")
try:
    download_file("media.zip", "media.zip")
    subprocess.run(["unzip", "-o", "media.zip", "-d", "/app/media"], check=True)
except Exception as e:
    print("no media.zip in google drive")

django.setup()

# Применяем миграции и собираем статику
print("Applying migrations...")
call_command("migrate", "--noinput")

print("Collecting static files...")
call_command("collectstatic", "--noinput")

# Создаем суперпользователя
print("Creating superuser...")
subprocess.run(["python", "manage.py", "shell", "<", "/app/create_superuser.py"], check=True)
print("Initialization complete.")
