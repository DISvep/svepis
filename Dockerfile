FROM python:3.12-slim-bullseye

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

RUN apt-get update && apt-get install -y gcc supervisor unzip && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

RUN ls -l entrypoint.sh

EXPOSE 8000
EXPOSE 5252

COPY supervisor.conf /etc/supervisor/conf.d/supervisor.conf

CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisor.conf"]
