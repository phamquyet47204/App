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

## Gửi email qua AWS Lambda + SES

Backend đã hỗ trợ gọi Lambda để gửi mail khi đăng ký/hủy môn.

### 1) Tạo Lambda gửi SES
- Mã Lambda mẫu: `aws/lambda/ses_mail_sender/lambda_function.py`
- Runtime: Python 3.12
- Region: `us-east-1`
- Biến môi trường Lambda:
   - `SES_REGION=us-east-1`
   - `FROM_EMAIL=abcuniversity@enormitpham.me`
   - `SES_SOURCE_ARN=arn:aws:ses:us-east-1:667467573689:identity/enormitpham.me`

### 2) Gán quyền cho Lambda role
Cho phép action `ses:SendEmail` trên identity:

```json
{
   "Version": "2012-10-17",
   "Statement": [
      {
         "Effect": "Allow",
         "Action": "ses:SendEmail",
         "Resource": "arn:aws:ses:us-east-1:667467573689:identity/enormitpham.me"
      }
   ]
}
```

### 3) Cấu hình backend gọi Lambda
Trong `.env`:

```dotenv
EMAIL_PROVIDER=lambda
EMAIL_LAMBDA_FUNCTION_NAME=course-registration-ses-mail-sender
EMAIL_LAMBDA_REGION=us-east-1
```

Với EC2/ECS chạy backend, IAM role cần quyền gọi Lambda (`lambda:InvokeFunction`) cho function trên.

## CI/CD với GitHub Actions (ECR + ECS)

Repo đã có sẵn workflows:
- `.github/workflows/ci.yml`: build kiểm tra backend/frontend cho PR.
- `.github/workflows/cd-ecs.yml`: build + push image lên ECR và deploy ECS khi merge `main`.

### GitHub Secrets cần tạo
- `AWS_ROLE_ARN`: IAM role cho GitHub OIDC để deploy AWS.

### GitHub Variables cần tạo
- `AWS_REGION` (ví dụ: `us-east-1`)
- `ECR_REPO_BE` (ví dụ: `be`)
- `ECR_REPO_FE` (ví dụ: `fe`)
- `ECS_CLUSTER`
- `ECS_SERVICE_BE`
- `ECS_SERVICE_FE`
- `ECS_CONTAINER_BE` (tên container backend trong task definition)
- `ECS_CONTAINER_FE` (tên container frontend trong task definition)
