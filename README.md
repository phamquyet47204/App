# Hệ thống đăng ký môn học (Django + React)

## Chức năng đã có
- Đăng nhập bằng MSSV hoặc email + mật khẩu
- Sinh viên xem môn đã đăng ký
- Sinh viên đăng ký/hủy đăng ký môn học
- Chỉ cho phép đăng ký trong khung thời gian mở
- Trang admin để bật/tắt và đặt thời gian đăng ký
- Gửi email thông báo khi đăng ký/hủy môn thành công
- Hỗ trợ AWS SES cho email
- Docker-ready

## Cấu trúc
- `backend/`: Django REST API
- `frontend/`: React + Vite
- `.env`: cấu hình môi trường
- `docker-compose.yml`: Docker orchestration

## Chạy nhanh với Docker (khuyên dùng)

```bash
docker-compose up --build
```

Truy cập:
- Frontend: http://localhost
- Backend: http://localhost:8000
- Admin: http://localhost:8000/admin

Xem chi tiết: [DOCKER.md](DOCKER.md)

## Chạy thủ công (development)
1. Tạo môi trường ảo và cài dependencies:
   - `cd backend`
   - `python -m venv .venv`
   - `.venv\\Scripts\\activate`
   - `pip install -r requirements.txt`
2. Tạo database:
   - `python manage.py makemigrations`
   - `python manage.py migrate`
3. Tạo admin/staff:
   - `python manage.py createsuperuser`
4. Chạy server:
   - `python manage.py runserver`

### Frontend
1. Cài package:
   - `cd frontend`
   - `npm install`
2. Chạy:
   - `npm run dev`

## Endpoint chính
- `POST /api/auth/login/`
- `POST /api/auth/logout/`
- `GET /api/auth/me/`
- `GET /api/courses/`
- `GET /api/registrations/`
- `POST /api/registrations/<course_id>/`
- `DELETE /api/registrations/<course_id>/`
- `GET /api/registration-window/`
- `GET/PUT /api/admin/registration-window/` (staff)

## Gợi ý tạo môn học
- Dùng Django Admin `http://localhost:8000/admin` để thêm `Course`
- Dùng admin đơn giản ở frontend (`/admin`) để mở/đóng đăng ký môn
- Hoặc import dữ liệu mẫu từ `seed_mysql.sql`

## Tài khoản mẫu (sau khi seed)
- **Sinh viên**: username `sv001` / password `Password123!`
- **Admin**: username `admin` / password `Admin123!`
