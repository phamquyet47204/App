# Backend + Frontend Documentation

## 1) Tong quan he thong

Day la he thong dang ky mon hoc gom 2 phan:

- Backend: Django + DRF, cung cap API
- Frontend: React + Vite, cung cap giao dien sinh vien/admin

## 2) Backend (Django + DRF)

### 2.1 Ky thuat

- Framework: Django + Django REST Framework
- Auth: Token Authentication (`rest_framework.authtoken`)
- Apps chinh: `accounts`, `courses`
- DB: MySQL (production) hoac SQLite (local)
- Email: SMTP hoac AWS Lambda (qua env)

### 2.2 Cau truc backend

- `backend/manage.py`: entrypoint
- `backend/config/settings.py`: cau hinh app, DB, CORS/CSRF, AWS Secrets
- `backend/config/urls.py`: root routes
- `backend/accounts/`: auth/login/me/logout, custom user
- `backend/courses/`: course, registration, registration-window, admin APIs

### 2.3 API backend

- `POST /api/auth/login/`
- `POST /api/auth/logout/`
- `GET /api/auth/me/`
- `GET /api/healthz/`
- `GET /api/courses/`
- `GET /api/registrations/`
- `POST /api/registrations/<course_id>/`
- `DELETE /api/registrations/<course_id>/`
- `GET /api/registration-window/`
- `GET /api/admin/registration-window/` (staff)
- `PUT /api/admin/registration-window/` (staff)
- `GET /api/admin/cpu-stress-test/` (staff)
- `POST /api/admin/cpu-stress-test/` (staff)

### 2.4 Chay backend local

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### 2.5 Bien moi truong backend

- Core: `DJANGO_SECRET_KEY`, `DJANGO_DEBUG`, `TIME_ZONE`
- DB: `DB_ENGINE`, `MYSQL_DB_HOST`, `MYSQL_DB_PORT`, `MYSQL_DB_NAME`, `MYSQL_DB_USER`, `MYSQL_DB_PASSWORD`
- AWS Secrets: `USE_AWS_SECRETS`, `AWS_SECRET_NAME`, `AWS_REGION`, `AWS_SECRETS_REQUIRED`
- CORS/CSRF: `CORS_ALLOWED_ORIGINS`, `CORS_ALLOW_ALL_ORIGINS`, `CSRF_TRUSTED_ORIGINS`
- Email: `EMAIL_PROVIDER`, `EMAIL_LAMBDA_FUNCTION_NAME`, `EMAIL_LAMBDA_REGION`

## 3) Frontend (React + Vite)

### 3.1 Ky thuat

- React + Vite
- Router: `react-router-dom`
- API helper: `frontend/src/api.js`
- Auth token luu trong `localStorage`

### 3.2 Cau truc frontend

- `frontend/src/main.jsx`: bootstrap app
- `frontend/src/App.jsx`: route + auth guard + login/logout flow
- `frontend/src/api.js`: fetch wrapper
- `frontend/src/pages/LoginPage.jsx`: man hinh dang nhap
- `frontend/src/pages/StudentPage.jsx`: man hinh sinh vien
- `frontend/src/pages/AdminPage.jsx`: man hinh admin

### 3.3 Chay frontend local

```bash
cd frontend
npm install
npm run dev
```

Mac dinh chay tai `http://localhost:5173`.

### 3.4 Bien moi truong frontend

- `VITE_API_BASE_URL` (mac dinh `/api`)

## 4) Luong nghiep vu tong the

1. User dang nhap bang MSSV/email + password
2. Frontend nhan token tu `/api/auth/login/` va luu localStorage
3. Frontend goi `/api/auth/me/` de xac nhan session
4. Sinh vien dang ky/huy mon qua `/api/registrations/<course_id>/`
5. Backend chi cho phep thao tac neu `RegistrationWindow.can_register()` la true
6. Admin cau hinh cua so dang ky qua `/api/admin/registration-window/`

## 5) Docker nhanh

### 5.1 Backend

```bash
cd backend
docker build -t app-backend:local .
docker run -p 8000:8000 --env-file ../.env app-backend:local
```

### 5.2 Frontend

```bash
cd frontend
docker build -t app-frontend:local .
docker run -p 80:80 app-frontend:local
```

## 6) Ghi chu deploy

- Tren ECS co the cho phep `ALLOWED_HOSTS=["*"]` khi:
  - chay trong ECS
  - `DJANGO_ALLOW_ALL_HOSTS_ON_ECS=true`
- Production nen dung MySQL/Aurora va AWS Secrets Manager.
