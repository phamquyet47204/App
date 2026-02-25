# Backend Dockerfile
FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    netcat-traditional \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Create entrypoint script
RUN echo '#!/bin/sh\n\
set -e\n\
DB_ENGINE=${DB_ENGINE:-sqlite}\n\
if [ "$DB_ENGINE" = "mysql" ]; then\n\
  DB_HOST=${MYSQL_DB_HOST:-127.0.0.1}\n\
  DB_PORT=${MYSQL_DB_PORT:-3306}\n\
  echo "Waiting for MySQL at ${DB_HOST}:${DB_PORT}..."\n\
  while ! nc -z "$DB_HOST" "$DB_PORT"; do\n\
    sleep 1\n\
  done\n\
  echo "MySQL is reachable."\n\
fi\n\
python manage.py migrate\n\
APP_PORT=${PORT:-8000}\n\
GUNICORN_WORKERS=${GUNICORN_WORKERS:-3}\n\
exec gunicorn config.wsgi:application --bind 0.0.0.0:${APP_PORT} --workers ${GUNICORN_WORKERS} --timeout 120\n\
' > /entrypoint.sh && chmod +x /entrypoint.sh

CMD ["/entrypoint.sh"]
