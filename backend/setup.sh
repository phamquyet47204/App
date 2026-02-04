#!/bin/bash

# Script setup cho backend

echo "=== Cài đặt Backend ==="

# Tạo virtual environment
echo "Tạo virtual environment..."
python -m venv venv

# Kích hoạt virtual environment
if [ -d "venv/Scripts" ]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Cài đặt dependencies
echo "Cài đặt dependencies..."
pip install -r requirements.txt

# Tạo file .env
if [ ! -f ".env" ]; then
    echo "Tạo file .env..."
    cp .env.example .env
    echo "Vui lòng chỉnh sửa file .env với thông tin của bạn"
fi

echo "=== Setup hoàn tất ==="
echo "Để bắt đầu, chạy lệnh:"
echo "  source venv/bin/activate  (Linux/Mac)"
echo "  venv\\Scripts\\activate  (Windows)"
echo "  python manage.py migrate"
echo "  python manage.py runserver"
