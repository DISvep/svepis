FROM python:3.12-slim-bullseye

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

RUN apt-get update && apt-get install -y gcc supervisor unzip && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

# Открываем порты
EXPOSE 8000
EXPOSE 5252

# Копируем ключ Google Drive
COPY gdrive_key.json /app/

# Копируем конфиг Supervisor
COPY supervisor.conf /etc/supervisor/conf.d/supervisor.conf

# Запускаем Supervisor
CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisor.conf"]
