FROM python:3.12-slim-bullseye

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV DJANGO_SETTINGS_MODULE=svepis.settings

WORKDIR /app

RUN apt-get update && apt-get install -y zip && apt-get install -y gcc supervisor unzip curl nginx && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

RUN chmod +x /app/entrypoint.sh

RUN mkdir -p /run/daphne && chown www-data:www-data

EXPOSE 5000

COPY supervisor.conf /etc/supervisor/conf.d/supervisor.conf

ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisor.conf"]
