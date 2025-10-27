# API HOÀN CHỈNH CHO STUDENT - DỰA TRÊN QUYỀN VÀ CLASS DIAGRAM

## 🔐 AUTHENTICATION APIs (Student có quyền sử dụng)

### 1. Đăng nhập Student
**API:** `POST /api/auth/student/login/`
**Payload:**
```json
{
  "username": "string",
  "password": "string"
}
```
**Response:**
```json
{
  "message": "Login successful",
  "session_key": "string",
  "user": {
    "userId": "string",
    "username": "string",
    "fullName": "string",
    "userType": "student"
  }
}
```

### 2. Đăng xuất
**API:** `POST /api/auth/logout/`
**Payload:** Không cần
**Response:**
```json
{
  "message": "Logout successful"
}
```

### 3. Đổi mật khẩu
**API:** `POST /api/auth/change-password/`
**Payload:**
```json
{
  "currentPassword": "string",
  "newPassword": "string"
}
```
**Response:**
```json
{
  "message": "Password changed successfully"
}
```

### 4. Kiểm tra session
**API:** `GET /api/auth/check-session/`
**Payload:** Không cần
**Response:**
```json
{
  "isValid": "boolean",
  "user": {
    "userId": "string",
    "username": "string",
    "userType": "student"
  }
}
```

## 🏠 DASHBOARD API

### 5. Dashboard Student
**API:** `GET /api/student/dashboard/`
**Payload:** Không cần
**Response:**
```json
{
  "student": {
    "studentId": "string",
    "studentCode": "string",
    "fullName": "string",
    "gpa": "number",
    "totalCredits": "number",
    "enrollmentYear": "number"
  },
  "currentSemester": {
    "semesterId": "string",
    "semesterName": "string"
  },
  "registeredCourses": "number",
  "unreadNotifications": "number"
}
```

## 📊 XEM ĐIỂM (view_grades permission)

### 6. Xem điểm của tôi
**API:** `GET /api/student/my-grades/`
**Payload:** Không cần
**Response:**
```json
{
  "grades": [
    {
      "gradeId": "string",
      "subject": {
        "subjectId": "string",
        "subjectCode": "string",
        "subjectName": "string",
        "credits": "number"
      },
      "courseClass": {
        "courseClassId": "string",
        "courseCode": "string",
        "courseName": "string"
      },
      "semester": {
        "semesterId": "string",
        "semesterName": "string"
      },
      "attendanceScore": "number",
      "assignmentScore": "number",
      "midtermScore": "number",
      "finalScore": "number",
      "totalScore": "number",
      "letterGrade": "string",
      "gradePoints": "number",
      "isPassed": "boolean"
    }
  ]
}
```



## 📝 ĐĂNG KÝ MÔN HỌC (register_course permission)

### 7. Xem môn học có thể đăng ký
**API:** `GET /api/services/registration/available-courses/{student_id}/`
**Payload:** Không cần (student ID trong URL)
**Response:**
```json
{
  "courses": [
    {
      "courseClassId": "string",
      "courseCode": "string",
      "courseName": "string",
      "subject": {
        "subjectId": "string",
        "subjectCode": "string",
        "subjectName": "string",
        "credits": "number"
      },
      "teacher": {
        "teacherId": "string",
        "fullName": "string"
      },
      "schedule": "string",
      "room": "string",
      "availableSlots": "number",
      "maxStudents": "number"
    }
  ]
}
```

### 8. Kiểm tra môn tiên quyết
**API:** `POST /api/services/registration/check-prerequisites/`
**Payload:**
```json
{
  "studentId": "string",
  "subjectId": "string"
}
```
**Response:**
```json
{
  "canRegister": "boolean",
  "missingPrerequisites": [
    {
      "subjectId": "string",
      "subjectCode": "string",
      "subjectName": "string"
    }
  ]
}
```

### 9. Kiểm tra xung đột lịch học
**API:** `POST /api/services/registration/check-schedule-conflict/`
**Payload:**
```json
{
  "studentId": "string",
  "courseClassId": "string"
}
```
**Response:**
```json
{
  "hasConflict": "boolean",
  "conflicts": [
    {
      "courseCode": "string",
      "courseName": "string",
      "schedule": "string"
    }
  ]
}
```

### 10. Đăng ký môn học
**API:** `POST /api/crud/registrations/create/`
**Payload:**
```json
{
  "registrationId": "string",
  "studentId": "string",
  "courseClassId": "string",
  "semesterId": "string"
}
```
**Response:**
```json
{
  "message": "Course registered successfully",
  "registrationId": "string"
}
```

## 🗓️ XEM LỊCH HỌC (view_schedule permission)

### 11. Xem lịch học của tôi
**API:** `GET /api/student/my-schedule/`
**Payload:** Không cần
**Response:**
```json
{
  "schedule": [
    {
      "courseClassId": "string",
      "courseCode": "string",
      "courseName": "string",
      "teacher": "string",
      "room": "string",
      "dayOfWeek": "string",
      "startTime": "string",
      "endTime": "string"
    }
  ]
}
```

### 12. Xem danh sách đăng ký của tôi
**API:** `GET /api/student/my-registrations/`
**Payload:** Không cần
**Response:**
```json
{
  "registrations": [
    {
      "registrationId": "string",
      "courseClass": {
        "courseClassId": "string",
        "courseCode": "string",
        "courseName": "string"
      },
      "semester": {
        "semesterId": "string",
        "semesterName": "string"
      },
      "registrationDate": "string",
      "status": "string"
    }
  ]
}
```

## 📄 YÊU CẦU TÀI LIỆU (request_document permission)

### 14. Tạo yêu cầu tài liệu
**API:** `POST /api/crud/document-requests/create/`
**Payload:**
```json
{
  "requestId": "string",
  "documentTypeId": "string",
  "semesterId": "string",
  "purpose": "string",
  "studentIds": ["string"]
}
```
**Response:**
```json
{
  "message": "Document request created",
  "requestId": "string"
}
```

### 15. Xem yêu cầu tài liệu của tôi
**API:** `GET /api/student/my-document-requests/`
**Payload:** Không cần
**Response:**
```json
{
  "documentRequests": [
    {
      "requestId": "string",
      "documentType": {
        "documentTypeId": "string",
        "name": "string",
        "processingDays": "number"
      },
      "semester": {
        "semesterId": "string",
        "semesterName": "string"
      },
      "requestDate": "string",
      "purpose": "string",
      "status": "string",
      "approvedDate": "string",
      "completedDate": "string"
    }
  ]
}
```

### 16. Xem loại tài liệu có thể yêu cầu
**API:** `GET /api/crud/document-types/`
**Payload:** Không cần
**Response:**
```json
{
  "documentTypes": [
    {
      "documentTypeId": "string",
      "name": "string",
      "code": "string",
      "description": "string",
      "maxRequestsPerSemester": "number",
      "processingDays": "number"
    }
  ]
}
```

## 💰 XEM HỌC PHÍ (view_tuition permission)

### 17. Xem học phí của tôi
**API:** `GET /api/student/my-tuition-fees/`
**Payload:** Không cần
**Response:**
```json
{
  "tuitionFees": [
    {
      "tuitionFeeId": "string",
      "semester": {
        "semesterId": "string",
        "semesterName": "string"
      },
      "totalCredits": "number",
      "feePerCredit": "number",
      "totalAmount": "number",
      "paidAmount": "number",
      "remainingAmount": "number",
      "paymentStatus": "string",
      "dueDate": "string",
      "isOverdue": "boolean"
    }
  ]
}
```

## 🔔 THÔNG BÁO

### 18. Xem thông báo chưa đọc
**API:** `GET /api/services/notifications/unread/`
**Payload:** Không cần
**Response:**
```json
{
  "notifications": [
    {
      "notificationId": "string",
      "title": "string",
      "content": "string",
      "notificationType": "string",
      "priority": "string",
      "scheduledAt": "string",
      "deliveredAt": "string"
    }
  ]
}
```

### 19. Đánh dấu thông báo đã đọc
**API:** `POST /api/services/notifications/{notification_id}/mark-read/`
**Payload:** Không cần (notification ID trong URL)
**Response:**
```json
{
  "message": "Notification marked as read"
}
```

### 20. Xem tất cả thông báo
**API:** `GET /api/student/my-notifications/`
**Payload:** Không cần
**Response:**
```json
{
  "notifications": [
    {
      "notificationId": "string",
      "title": "string",
      "content": "string",
      "notificationType": "string",
      "priority": "string",
      "scheduledAt": "string",
      "readAt": "string",
      "isRead": "boolean"
    }
  ]
}
```

## 👤 QUẢN LÝ THÔNG TIN CÁ NHÂN

### 21. Xem thông tin cá nhân
**API:** `GET /api/student/profile/`
**Payload:** Không cần
**Response:**
```json
{
  "student": {
    "studentId": "string",
    "studentCode": "string",
    "user": {
      "userId": "string",
      "username": "string",
      "email": "string",
      "fullName": "string",
      "phone": "string"
    },
    "studentClass": {
      "classId": "string",
      "className": "string",
      "major": {
        "majorId": "string",
        "majorName": "string",
        "department": {
          "departmentId": "string",
          "departmentName": "string"
        }
      }
    },
    "dateOfBirth": "string",
    "gender": "string",
    "enrollmentYear": "number",
    "gpa": "number",
    "totalCredits": "number"
  }
}
```

### 22. Cập nhật thông tin cá nhân
**API:** `PUT /api/student/profile/update/`
**Payload:**
```json
{
  "fullName": "string",
  "email": "string",
  "phone": "string"
}
```
**Response:**
```json
{
  "message": "Profile updated successfully"
}
```

## 📚 XEM THÔNG TIN KHOA/NGÀNH/MÔN HỌC (Read-only)

### 23. Xem danh sách khoa
**API:** `GET /api/crud/departments/`
**Payload:** Không cần
**Response:**
```json
{
  "departments": [
    {
      "departmentId": "string",
      "departmentCode": "string",
      "departmentName": "string",
      "status": "string"
    }
  ]
}
```

### 24. Xem danh sách ngành
**API:** `GET /api/crud/majors/`
**Payload:** Không cần
**Response:**
```json
{
  "majors": [
    {
      "majorId": "string",
      "majorCode": "string",
      "majorName": "string",
      "department": "string",
      "durationYears": "number",
      "totalCredits": "number"
    }
  ]
}
```

### 25. Xem danh sách môn học
**API:** `GET /api/crud/subjects/`
**Payload:** Không cần
**Response:**
```json
{
  "subjects": [
    {
      "subjectId": "string",
      "subjectCode": "string",
      "subjectName": "string",
      "department": "string",
      "credits": "number",
      "theoryHours": "number",
      "practiceHours": "number"
    }
  ]
}
```

### 26. Xem danh sách lớp học phần
**API:** `GET /api/crud/course-classes/`
**Payload:** Không cần
**Response:**
```json
{
  "course_classes": [
    {
      "courseClassId": "string",
      "courseCode": "string",
      "courseName": "string",
      "subject": "string",
      "teacher": "string",
      "semester": "string",
      "room": "string",
      "maxStudents": "number",
      "currentStudents": "number"
    }
  ]
}
```

### 27. Xem danh sách học kỳ
**API:** `GET /api/crud/semesters/`
**Payload:** Không cần
**Response:**
```json
{
  "semesters": [
    {
      "semesterId": "string",
      "semesterCode": "string",
      "semesterName": "string",
      "academicYear": "string",
      "startDate": "string",
      "endDate": "string"
    }
  ]
}
```

---

## 📋 TỔNG KẾT QUYỀN STUDENT

### **Student Permissions từ permissions.py:**
- `view_grades` - Xem điểm
- `register_course` - Đăng ký môn học  
- `drop_course` - Hủy đăng ký môn học
- `view_schedule` - Xem lịch học
- `request_document` - Yêu cầu tài liệu
- `view_tuition` - Xem học phí

### **Tổng số API cho Student: 26**
- **Authentication**: 4 APIs
- **Dashboard**: 1 API
- **Grades**: 1 API
- **Course Registration**: 4 APIs
- **Schedule**: 2 APIs
- **Document Requests**: 3 APIs
- **Tuition Fees**: 1 API
- **Notifications**: 3 APIs
- **Profile Management**: 2 APIs
- **Read-only Information**: 5 APIs

### **Base URL:**
```
http://127.0.0.1:8000/api/
```

### **Authentication Header:**
```
Authorization: Session {session_key}
X-Session-Key: {session_key}
```
