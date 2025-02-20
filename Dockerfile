FROM python:3.12-slim-bullseye

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV DJANGO_SETTINGS_MODULE=svepis.settings

WORKDIR /app

# Установить необходимые пакеты
RUN apt-get update && apt-get install -y zip && apt-get install -y gcc supervisor unzip curl && rm -rf /var/lib/apt/lists/*

# Копируем requirements.txt и устанавливаем зависимости
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект в контейнер
COPY . /app/

RUN chmod +x /app/entrypoint.sh

# Открываем порты
EXPOSE 8000
EXPOSE 5252

# Копируем конфиг supervisor
COPY supervisor.conf /etc/supervisor/conf.d/supervisor.conf

# Запуск supervisor
ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisor.conf"]
