# Hướng dẫn chạy với Docker

## Chạy toàn bộ hệ thống

```bash
docker-compose up --build
```

Truy cập:
- Frontend: http://localhost
- Backend API: http://localhost:8000
- Django Admin: http://localhost:8000/admin

## Chạy riêng lẻ

**Backend only:**
```bash
cd backend
docker build -t course-backend .
docker run -p 8000:8000 --env-file ../.env course-backend
```

**Frontend only:**
```bash
cd frontend
docker build -t course-frontend .
docker run -p 80:80 course-frontend
```

## Seed dữ liệu vào MySQL RDS

```bash
MYSQL_PWD='python123' mysql --ssl -h database-1-instance-1.cex04as4isj0.us-east-1.rds.amazonaws.com -P 3306 -u admin course_registration < sql.sql
```

## Tạo superuser

```bash
docker exec -it course-registration-backend python manage.py createsuperuser
```

## Dừng và xóa containers

```bash
docker-compose down
```

## Xóa cả volumes (database)

```bash
docker-compose down -v
```

## Production tips

1. Thay `DJANGO_SECRET_KEY` trong `.env`
2. Đặt `DJANGO_DEBUG=False`
3. Cấu hình HTTPS cho nginx
4. Sử dụng managed database (RDS) như cấu hình hiện tại

## Gửi mail qua Lambda (thay SMTP trực tiếp)

1. Triển khai Lambda theo mã tại `aws/lambda/ses_mail_sender/lambda_function.py`
2. Đặt `.env` backend:

```dotenv
EMAIL_PROVIDER=lambda
EMAIL_LAMBDA_FUNCTION_NAME=course-registration-ses-mail-sender
EMAIL_LAMBDA_REGION=us-east-1
```

3. IAM role của máy/container chạy backend cần quyền:
- `lambda:InvokeFunction` cho Lambda mail sender

4. Rebuild services:

```bash
docker-compose up -d --build
```
