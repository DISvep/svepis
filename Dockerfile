FROM python:3.12-slim-bullseye

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Установить необходимые пакеты
RUN apt-get update && apt-get install -y gcc supervisor unzip curl && rm -rf /var/lib/apt/lists/*

# Копируем requirements.txt и устанавливаем зависимости
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект в контейнер
COPY . /app/

RUN echo ${GDRIVE_KEY}
RUN python init_app.py
ENV GDRIVE_KEY=${GDRIVE_KEY}

# Открываем порты
EXPOSE 8000
EXPOSE 5252

# Копируем конфиг supervisor
COPY supervisor.conf /etc/supervisor/conf.d/supervisor.conf

# Запуск supervisor
CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisor.conf"]
