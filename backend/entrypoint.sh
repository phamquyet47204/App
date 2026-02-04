#!/bin/bash

# Exit on error
set -e

echo "Waiting for database..."
# Wait for database to be ready
python << END
import sys
import time
import os
import mysql.connector
from mysql.connector import Error

max_retries = 30
retry_count = 0

while retry_count < max_retries:
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            port=os.getenv('DB_PORT', '3306'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', ''),
            database=os.getenv('DB_NAME', 'course_registration')
        )
        if connection.is_connected():
            print("Database is ready!")
            connection.close()
            sys.exit(0)
    except Error as e:
        retry_count += 1
        print(f"Database not ready yet (attempt {retry_count}/{max_retries}). Waiting...")
        time.sleep(2)

print("Could not connect to database after maximum retries")
sys.exit(1)
END

echo "Running migrations..."
python manage.py makemigrations --noinput
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting server..."
exec "$@"
