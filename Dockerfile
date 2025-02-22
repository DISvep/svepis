FROM python:3.12-slim-bullseye

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DJANGO_SETTINGS_MODULE=svepis.settings

WORKDIR /app

RUN apt-get update && apt-get install -y \
    zip gcc supervisor unzip curl nginx \
    build-essential python3-dev && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/
RUN chmod +x /app/entrypoint.sh

RUN mkdir -p /run/daphne/

EXPOSE 8000 443

# COPY supervisor.conf /etc/supervisor/conf.d/supervisor.conf

ENTRYPOINT ["/app/entrypoint.sh"]
# CMD ["supervisord", "-n", "-c", "/etc/supervisor/conf.d/supervisor.conf"]
CMD daphne -b 0.0.0.0 -p 443 svepis.asgi:application
