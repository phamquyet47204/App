# TEST API VOI POSTMAN

## BUOC 1: TAO USER TEST

### Cach 1: Qua Django Shell (Nhanh nhat)
```bash
python manage.py shell
```

```python
from core.models import User

# Tao admin
User.objects.create_user(
    username='admin',
    password='admin123',
    email='admin@test.com',
    full_name='Admin User',
    user_type='admin',
    status='active'
)

# Tao teacher
User.objects.create_user(
    username='teacher',
    password='teacher123',
    email='teacher@test.com',
    full_name='Teacher User',
    user_type='teacher',
    status='active'
)

# Tao student
User.objects.create_user(
    username='student',
    password='student123',
    email='student@test.com',
    full_name='Student User',
    user_type='student',
    status='active'
)

# Kiem tra
User.objects.all().values('username', 'user_type', 'status')
```

Nhan Ctrl+Z (Windows) hoac Ctrl+D (Mac/Linux) de thoat

---

## BUOC 2: CHAY SERVER

```bash
python manage.py runserver
```

Server chay tai: http://localhost:8000

---

## BUOC 3: TEST VOI POSTMAN

### 3.1. DANG NHAP

**Request:**
- Method: `POST`
- URL: `http://localhost:8000/api/auth/login/`
- Headers:
  - `Content-Type: application/json`
- Body (raw JSON):
```json
{
    "username": "admin",
    "password": "admin123"
}
```

**Response (200 OK):**
```json
{
    "message": "Login successful",
    "session_key": "abc123xyz...",
    "user": {
        "username": "admin",
        "email": "admin@test.com",
        "full_name": "Admin User",
        "user_type": "admin"
    }
}
```

**LUU Y:** Copy `session_key` de dung cho cac request tiep theo

---

### 3.2. KIEM TRA PHIEN

**Request:**
- Method: `GET`
- URL: `http://localhost:8000/api/auth/check-session/`
- Headers:
  - `Cookie: sessionid=<session_key_vua_copy>`

**Response (200 OK):**
```json
{
    "authenticated": true,
    "user": {
        "username": "admin",
        "user_type": "admin",
        "status": "active"
    }
}
```

---

### 3.3. ADMIN DASHBOARD

**Request:**
- Method: `GET`
- URL: `http://localhost:8000/api/admin/dashboard/`
- Headers:
  - `Cookie: sessionid=<session_key>`

**Response (200 OK):**
```json
{
    "message": "Welcome to admin dashboard"
}
```

---

### 3.4. QUAN LY USERS (Admin only)

**Request:**
- Method: `GET`
- URL: `http://localhost:8000/api/admin/manage-users/`
- Headers:
  - `Cookie: sessionid=<admin_session_key>`

**Response (200 OK):**
```json
{
    "users": [
        {
            "username": "admin",
            "email": "admin@test.com",
            "user_type": "admin",
            "status": "active"
        },
        {
            "username": "teacher",
            "email": "teacher@test.com",
            "user_type": "teacher",
            "status": "active"
        }
    ]
}
```

---

### 3.5. DOI MAT KHAU

**Request:**
- Method: `POST`
- URL: `http://localhost:8000/api/auth/change-password/`
- Headers:
  - `Content-Type: application/json`
  - `Cookie: sessionid=<session_key>`
- Body (raw JSON):
```json
{
    "old_password": "admin123",
    "new_password": "newpass123"
}
```

**Response (200 OK):**
```json
{
    "message": "Password changed successfully"
}
```

---

### 3.6. DAT LAI MAT KHAU

**Buoc 1: Yeu cau token**

**Request:**
- Method: `POST`
- URL: `http://localhost:8000/api/auth/request-reset/`
- Headers:
  - `Content-Type: application/json`
- Body (raw JSON):
```json
{
    "email": "admin@test.com"
}
```

**Response (200 OK):**
```json
{
    "message": "Reset token created",
    "token": "xyz789abc..."
}
```

**Buoc 2: Dat lai mat khau**

**Request:**
- Method: `POST`
- URL: `http://localhost:8000/api/auth/reset-password/`
- Headers:
  - `Content-Type: application/json`
- Body (raw JSON):
```json
{
    "token": "xyz789abc...",
    "new_password": "newpass456"
}
```

**Response (200 OK):**
```json
{
    "message": "Password reset successfully"
}
```

---

### 3.7. DANG XUAT

**Request:**
- Method: `POST`
- URL: `http://localhost:8000/api/auth/logout/`
- Headers:
  - `Cookie: sessionid=<session_key>`

**Response (200 OK):**
```json
{
    "message": "Logout successful"
}
```

---

## BUOC 4: TEST PHAN QUYEN

### 4.1. Teacher Truy Cap Teacher Dashboard

**Dang nhap teacher truoc:**
```json
POST http://localhost:8000/api/auth/login/
{
    "username": "teacher",
    "password": "teacher123"
}
```

**Truy cap dashboard:**
```
GET http://localhost:8000/api/teacher/dashboard/
Cookie: sessionid=<teacher_session_key>
```

**Response (200 OK):**
```json
{
    "message": "Welcome to teacher dashboard"
}
```

### 4.2. Teacher Khong Vao Duoc Admin Area

**Request:**
```
GET http://localhost:8000/api/admin/dashboard/
Cookie: sessionid=<teacher_session_key>
```

**Response (403 Forbidden):**
```json
{
    "error": "Access denied. Admin role required"
}
```

---

## CAC LOI THUONG GAP

### Loi 1: Method Not Allowed (405)
**Nguyen nhan:** Dung sai method (GET thay vi POST)
**Giai phap:** Kiem tra method dung chua

### Loi 2: Unauthorized (401)
**Nguyen nhan:** Chua dang nhap hoac session het han
**Giai phap:** Dang nhap lai, lay session_key moi

### Loi 3: Forbidden (403)
**Nguyen nhan:** Sai role hoac khong co permission
**Giai phap:** Dang nhap dung user co quyen

### Loi 4: Bad Request (400)
**Nguyen nhan:** Thieu field hoac sai format JSON
**Giai phap:** Kiem tra Body phai la raw JSON

---

## TIPS POSTMAN

### 1. Luu Session Key
- Sau khi login, copy session_key
- Tao Environment variable: `session_key`
- Dung: `{{session_key}}` trong Cookie header

### 2. Tao Collection
- Tao folder "Authentication"
- Them tat ca requests vao
- Share cho team

### 3. Pre-request Script
```javascript
// Tu dong login truoc moi request
pm.sendRequest({
    url: 'http://localhost:8000/api/auth/login/',
    method: 'POST',
    header: {'Content-Type': 'application/json'},
    body: {
        mode: 'raw',
        raw: JSON.stringify({
            username: 'admin',
            password: 'admin123'
        })
    }
}, function (err, res) {
    pm.environment.set('session_key', res.json().session_key);
});
```

### 4. Tests Script
```javascript
// Kiem tra response
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Response has message", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData).to.have.property('message');
});
```

---

## CHECKLIST

- [ ] Server dang chay (python manage.py runserver)
- [ ] Da tao user test
- [ ] Postman da cai dat
- [ ] Method la POST cho login
- [ ] Header co Content-Type: application/json
- [ ] Body la raw JSON
- [ ] Da copy session_key sau login
- [ ] Dung Cookie header cho cac request can auth

---

**XONG!** ✅
