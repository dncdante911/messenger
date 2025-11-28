#!/bin/bash
# start.sh

# Получаем переменные подключения из .env через настройки Dockerfile
DB_HOST=${DB_HOST:-db}
DB_PORT=${DB_PORT:-5432}

echo "Ожидание старта PostgreSQL на $DB_HOST:$DB_PORT..."

# Используем netcat (nc) для проверки доступности порта.
# Dockerfile должен включать установку netcat (nc).
# Например: RUN apt-get update && apt-get install -y netcat-openbsd
while ! nc -z $DB_HOST $DB_PORT; do
  sleep 0.5
done

echo "База данных PostgreSQL запущена. Запуск приложения..."

# Запуск Uvicorn
exec uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4