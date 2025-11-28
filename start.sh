#!/bin/bash
# start.sh: Надежный запуск Uvicorn/FastAPI

# 1. Надежная проверка доступности порта DB
DB_HOST=\${DB_HOST:-db}
DB_PORT=\${DB_PORT:-5432}

echo "--- ? Ожидание запуска PostgreSQL на \${DB_HOST}:\${DB_PORT}... ---"
for i in {1..50}; do
  if nc -z \${DB_HOST} \${DB_PORT}; then
    echo "--- ? PostgreSQL доступен. ---"
    break
  fi
  sleep 0.5
done

if ! nc -z \${DB_HOST} \${DB_PORT}; then
  echo "--- ? Ошибка: PostgreSQL недоступен после всех попыток. Выход. ---"
  exit 1
fi

# 2. Однократная инициализация БД с повторами для устойчивости сети
echo "--- ?? Шаг 1/2: Запуск db_init.py для создания схемы БД (с повторами)... ---"
MAX_ATTEMPTS=5
ATTEMPT=1
INIT_SUCCESS=false

while [ \$ATTEMPT -le \$MAX_ATTEMPTS ]; do
  # Мы используем python3, так как 'python' может быть недоступен в некоторых контейнерах
  # Если это не сработает, замените python3 на python.
  python3 /app/db_init.py 
  if [ \$? -eq 0 ]; then
    INIT_SUCCESS=true
    break
  else
    echo "--- ? db_init.py завершился с ошибкой (Попытка №\$ATTEMPT). Ожидание 3 секунды... ---"
    ATTEMPT=\$((ATTEMPT + 1))
    sleep 3
  fi
done

if [ "\$INIT_SUCCESS" = false ]; then
    echo "--- ?? Критическая ошибка: Не удалось инициализировать БД. Выход. ---"
    exit 1
fi

echo "--- ?? Шаг 2/2: Запуск Uvicorn в основном многопоточном режиме (4 воркера)... ---"

# 3. Запуск основного многопоточного приложения
exec uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4