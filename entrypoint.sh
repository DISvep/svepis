#!/bin/sh

set -e  # Остановить выполнение при ошибке

echo "Decoding Google Drive key..."
echo $GDRIVE_KEY | base64 -d > /app/gdrive_key.json || echo "Failed to decode Google Drive key."

echo "Downloading database from Google Drive..."
python -c 'from gdrive_utils import download_file; download_file("db.sqlite3", "db.sqlite3")' || echo "Failed to download database."

echo "Downloading media files from Google Drive..."
python -c 'from gdrive_utils import download_file; download_file("media.zip", "media.zip")' || echo "Failed to download media."

echo "Extracting media files..."
unzip -o media.zip -d /app/media || echo "No media.zip found, skipping extraction."

echo "Applying migrations..."
python manage.py migrate --noinput || echo "Migration failed."

echo "Collecting static files..."
python manage.py collectstatic --noinput || echo "Static collection failed."

echo "Creating superuser..."
python manage.py shell < /app/create_superuser.py || echo "Superuser creation failed."

echo "Initialization complete."
exec "$@"  # Выполнение следующей команды в supervisor
