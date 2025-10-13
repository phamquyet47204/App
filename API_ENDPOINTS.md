# API ENDPOINTS - STUDENT MANAGEMENT SYSTEM

## AUTHENTICATION ENDPOINTS

### 1. Admin Login (Chỉ Admin)
```
POST /api/auth/admin/login/
Body: {"username": "admin", "password": "python123"}
Response: {"message": "Admin login successful", "session_key": "...", "user": {...}}
Error 403: Nếu không phải admin
```

### 2. Teacher Login (Chỉ Teacher)
```
POST /api/auth/teacher/login/
Body: {"username": "teacher1", "password": "python123"}
Response: {"message": "Teacher login successful", "session_key": "...", "user": {...}}
Error 403: Nếu không phải teacher
```

### 3. Student Login (Chỉ Student)
```
POST /api/auth/student/login/
Body: {"username": "student1", "password": "python123"}
Response: {"message": "Student login successful", "session_key": "...", "user": {...}}
Error 403: Nếu không phải student
```

### 4. Logout
```
POST /api/auth/logout/
Cookie: sessionid=<session_key>
Response: {"message": "Logout successful"}
```

### 6. Change Password
```
POST /api/auth/change-password/
Cookie: sessionid=<session_key>
Body: {"old_password": "...", "new_password": "..."}
Response: {"message": "Password changed successfully"}
```

### 7. Request Password Reset
```
POST /api/auth/request-reset/
Body: {"email": "admin@test.com"}
Response: {"message": "Reset token created", "token": "..."}
```

### 8. Reset Password
```
POST /api/auth/reset-password/
Body: {"token": "...", "new_password": "..."}
Response: {"message": "Password reset successfully"}
```

### 9. Check Session
```
GET /api/auth/check-session/
Cookie: sessionid=<session_key>
Response: {"authenticated": true, "user": {...}}
```

## DASHBOARD ENDPOINTS

### 10. Admin Dashboard
```
GET /api/admin/dashboard/
Cookie: sessionid=<session_key>
Response: {"message": "Welcome to admin dashboard"}
Requires: Admin role
```

### 11. Teacher Dashboard
```
GET /api/teacher/dashboard/
Cookie: sessionid=<session_key>
Response: {"message": "Welcome to teacher dashboard"}
Requires: Teacher role
```

### 12. Student Dashboard
```
GET /api/student/dashboard/
Cookie: sessionid=<session_key>
Response: {"message": "Welcome to student dashboard"}
Requires: Student role
```

## PERMISSION-BASED ENDPOINTS

### 13. Manage Users
```
GET /api/admin/manage-users/
Cookie: sessionid=<session_key>
Response: {"users": [...]}
Requires: Admin + permission 'manage_users'
```

### 14. Input Grades
```
POST /api/teacher/input-grades/
Cookie: sessionid=<session_key>
Response: {"message": "Grade input functionality"}
Requires: Teacher + permission 'input_grades'
```

### 15. View My Grades
```
GET /api/student/my-grades/
Cookie: sessionid=<session_key>
Response: {"message": "Student grades view"}
Requires: Student + permission 'view_grades'
```

### 16. Approve Document
```
POST /api/admin/approve-document/
Cookie: sessionid=<session_key>
Response: {"message": "Document approval functionality"}
Requires: Admin + permission 'approve_documents'
```

---

##

Tất cả users có password: **python123**

- Admin: `admin`
- Teacher: `teacher1`, `teacher2`
- Student: `student1`, `student2`, `student3`

---

## MIDDLEWARE FLOW

1. **SessionValidationMiddleware** - Kiểm tra session hợp lệ
2. **AuthenticationMiddleware** - Kiểm tra user đã đăng nhập và active
3. **RolePermissionMiddleware** - Kiểm tra role theo path

### Exempt Paths (Không cần authentication):
- `/api/auth/login/`
- `/api/auth/admin/login/`
- `/api/auth/teacher/login/`
- `/api/auth/student/login/`
- `/api/auth/logout/`
- `/api/auth/request-reset/`
- `/api/auth/reset-password/`
- `/admin/`
- `/static/`
