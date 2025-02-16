FROM python:3.12-slim-bullseye

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

EXPOSE 8000

CMD sh -c "python manage.py migrate && python manage.py collectstatic --noinput && python manage.py shell -c 'from django.contrib.auth import get_user_model; User = get_user_model(); import os; username = os.getenv(\"DJANGO_SUPERUSER_USERNAME\"); email = os.getenv(\"DJANGO_SUPERUSER_EMAIL\"); password = os.getenv(\"DJANGO_SUPERUSER_PASSWORD\"); if not User.objects.filter(username=username).exists(): User.objects.create_superuser(username, email, password); print(\"Superuser created\"); else: print(\"Superuser already exists\")' && gunicorn your_project_name.wsgi -b 0.0.0.0:8000"
