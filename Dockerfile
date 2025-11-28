FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y netcat-openbsd && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["sh", "-c", "echo 'Waiting for DB...' && while ! nc -z ${DB_HOST:-db} ${DB_PORT:-5432}; do sleep 1; done && echo 'Starting app...' && uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4"]