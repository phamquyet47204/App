## TOM TAT HE THONG XAC THUC

### TONG QUAN

He thong xac thuc hoan chinh voi:
- ✅ Dang nhap/Dang xuat
- ✅ Doi mat khau
- ✅ Dat lai mat khau
- ✅ Quan ly phien (Session)
- ✅ Phan quyen theo vai tro (Admin/Teacher/Student)
- ✅ Middleware tu dong kiem tra

---

## CAU TRUC FILE

```
core/
├── models.py              # User, PasswordResetToken
├── authentication.py      # AuthenticationService
├── permissions.py         # RolePermission, decorators
├── middleware.py          # 3 middleware
├── views.py              # API endpoints
├── urls.py               # URL routing
├── tests.py              # 20 test cases
└── admin.py              # Django admin
```

---

## API ENDPOINTS

### 1. Dang Nhap
```
POST /api/auth/login/
Body: {"username": "admin", "password": "admin123"}
Response: {"message": "Login successful", "session_key": "...", "user": {...}}
```

### 2. Dang Xuat
```
POST /api/auth/logout/
Cookie: sessionid=<session_key>
Response: {"message": "Logout successful"}
```

### 3. Doi Mat Khau
```
POST /api/auth/change-password/
Cookie: sessionid=<session_key>
Body: {"old_password": "...", "new_password": "..."}
Response: {"message": "Password changed successfully"}
```

### 4. Dat Lai Mat Khau
```
# Buoc 1: Yeu cau token
POST /api/auth/request-reset/
Body: {"email": "admin@test.com"}
Response: {"message": "Reset token created", "token": "..."}

# Buoc 2: Dat lai mat khau
POST /api/auth/reset-password/
Body: {"token": "...", "new_password": "..."}
Response: {"message": "Password reset successfully"}
```

### 5. Kiem Tra Phien
```
GET /api/auth/check-session/
Cookie: sessionid=<session_key>
Response: {"authenticated": true, "user": {...}}
```

### 6. Dashboards
```
GET /api/admin/dashboard/     # Admin only
GET /api/teacher/dashboard/   # Teacher only
GET /api/student/dashboard/   # Student only
```

### 7. Quan Ly Users
```
GET /api/admin/manage-users/  # Admin + permission 'manage_users'
Response: {"users": [...]}
```

---

## MIDDLEWARE (3 lop bao mat)

### 1. SessionValidationMiddleware
- Kiem tra session con hieu luc
- Tu dong xoa session het han

### 2. AuthenticationMiddleware
- Kiem tra user da dang nhap
- Kiem tra status = 'active'
- Exempt: /api/auth/*, /admin/, /static/

### 3. RolePermissionMiddleware
- /api/admin/* → chi admin
- /api/teacher/* → chi teacher
- /api/student/* → chi student

---

## PHAN QUYEN

### Admin (8 quyen)
- manage_users
- manage_departments
- manage_subjects
- generate_reports
- backup_system
- configure_system
- approve_documents
- manage_tuition

### Teacher (5 quyen)
- view_assigned_classes
- input_grades
- export_grades
- take_attendance
- view_students

### Student (6 quyen)
- view_grades
- register_course
- drop_course
- view_schedule
- request_document
- view_tuition

---

## CACH SU DUNG

### 1. Tao User
```bash
python manage.py shell
```
```python
from core.models import User
User.objects.create_user(
    username='admin',
    password='admin123',
    email='admin@test.com',
    full_name='Admin User',
    user_type='admin',
    status='active'
)
```

### 2. Chay Server
```bash
python manage.py runserver
```

### 3. Test voi Postman
- POST /api/auth/login/ → Lay session_key
- Dung session_key trong Cookie header
- Test cac endpoints khac

---

## LUONG HOAT DONG

### Dang Nhap
```
1. POST /api/auth/login/ {username, password}
2. AuthenticationService.authenticate_user()
3. Kiem tra status = 'active'
4. AuthenticationService.create_session()
5. Tra ve session_key
```

### Truy Cap API
```
1. Request voi Cookie: sessionid=<session_key>
2. SessionValidationMiddleware: Kiem tra session
3. AuthenticationMiddleware: Kiem tra authenticated + active
4. RolePermissionMiddleware: Kiem tra role theo path
5. View: Decorator kiem tra permission cu the
6. Response
```

### Dat Lai Mat Khau
```
1. POST /api/auth/request-reset/ {email}
2. Tao PasswordResetToken (het han 24h)
3. Tra ve token
4. POST /api/auth/reset-password/ {token, new_password}
5. Xac thuc token
6. Dat mat khau moi
7. Danh dau token da dung
```

---

## BAO MAT

### Password
- Hash bang PBKDF2
- Khong luu nguyen ban

### Session
- Het han sau 1 gio
- HTTPOnly cookie
- SameSite = 'Lax'

### Token Reset
- Het han sau 24h
- Chi dung 1 lan
- Random 32 bytes

### Status Check
- Chi user active moi dang nhap

---

## TEST

### Chay Tests
```bash
# Tat ca tests
python manage.py test core

# Test cu the
python manage.py test core.tests.AuthenticationTestCase

# Test flow
python test_authentication_flow.py
```

### Ket Qua
- 20/20 tests PASS ✅
- AuthenticationTestCase: 10 tests
- RolePermissionTestCase: 7 tests
- SessionManagementTestCase: 3 tests

---

## CAU HINH (settings.py)

```python
AUTH_USER_MODEL = 'core.User'
LOGIN_URL = '/api/auth/login/'

MIDDLEWARE = [
    ...
    'core.middleware.SessionValidationMiddleware',
    'core.middleware.AuthenticationMiddleware',
    'core.middleware.RolePermissionMiddleware',
]

SESSION_COOKIE_AGE = 3600  # 1 gio
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'

PASSWORD_RESET_TIMEOUT = 86400  # 24 gio
```

---

## LOI THUONG GAP

### 1. Loi 401 - Unauthorized
- Chua dang nhap
- Session het han
→ Dang nhap lai

### 2. Loi 403 - Forbidden
- Sai role
- Khong co permission
- User inactive
→ Kiem tra role va status

### 3. Loi 405 - Method Not Allowed
- Dung sai method (GET thay vi POST)
→ Kiem tra method

### 4. CSRF Error
- Thieu CSRF token
→ Da them @csrf_exempt cho cac API

### 5. Session Key = null
- Session khong duoc tao
→ Da fix: force save session

---

## QUAN TRONG

### User vs Student/Teacher/Admin
- **User**: Tai khoan dang nhap (username, password, user_type)
- **Student/Teacher/Admin**: Thong tin chi tiet

→ Can tao CA HAI:
```python
# Tao User
user = User.objects.create_user(...)

# Tao Student
Student.objects.create(user=user, ...)
```

### Middleware vs Decorators
- **Middleware**: Kiem tra CHUNG theo PATH
- **Decorators**: Kiem tra CHI TIET theo PERMISSION

→ Dung CA HAI de bao mat 2 lop

---

## CHECKLIST

- [x] Models: User, PasswordResetToken
- [x] Authentication Service
- [x] Permissions & Decorators
- [x] 3 Middleware
- [x] API Endpoints
- [x] Tests (20/20 PASS)
- [x] Django Admin
- [x] Documentation


---

## TOM TAT NHANH

### Tao User
```bash
python manage.py shell
from core.models import User
User.objects.create_user(username='admin', password='admin123', user_type='admin', status='active')
```

### Test API
```bash
# Login
POST /api/auth/login/
Body: {"username": "admin", "password": "admin123"}

# Dung session_key trong Cookie
Cookie: sessionid=<session_key>
```

### Chay Test
```bash
python manage.py test core
```

---

