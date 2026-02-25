# Backend Dockerfile
FROM python:3.12-slim

WORKDIR /app

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
python manage.py runserver 0.0.0.0:8000\n\
' > /entrypoint.sh && chmod +x /entrypoint.sh

CMD ["/entrypoint.sh"]
