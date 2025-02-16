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

# Запуск миграций, создание суперпользователя и запуск gunicorn
CMD sh -c "python manage.py migrate && python manage.py collectstatic --noinput && python manage.py shell < /app/create_superuser.py && gunicorn svepis.wsgi -b 0.0.0.0:8000"
