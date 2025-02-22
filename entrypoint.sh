#!/bin/sh
set -e

echo "Checking environment variables..."
if [ -z "$GDRIVE_KEY" ]; then
  echo "ERROR: GDRIVE_KEY is missing!"
  exit 1
fi

echo "Starting init_app.py..."
python /app/init_app.py

echo "Starting Supervisor..."
exec "$@"
