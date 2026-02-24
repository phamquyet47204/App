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

## Seed dữ liệu vào MySQL container

```bash
docker exec -i course-registration-db mysql -uroot -ppython123 course_registration < seed_mysql.sql
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
4. Sử dụng managed database thay vì MySQL container
