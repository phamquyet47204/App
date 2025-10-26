# API VÀ PAYLOAD CHO CHỨC NĂNG STUDENT

## 1. XEM LỚP HỌC

### API: `GET /api/crud/course-classes/`
**Payload:** Không cần payload (GET request)

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

## 2. XEM ĐIỂM VÀ KẾT QUẢ HỌC TẬP

### API: `GET /api/student/my-grades/`
**Payload:** Không cần payload

**Response:**
```json
{
  "grades": [
    {
      "gradeId": "string",
      "subject": "string",
      "courseClass": "string", 
      "semester": "string",
      "assignmentScore": "number",
      "midtermScore": "number",
      "finalScore": "number",
      "averageScore": "number",
      "letterGrade": "string",
      "gradePoint": "number",
      "isPassed": "boolean"
    }
  ]
}
```

### API: `POST /api/services/grades/calculate-gpa/`
**Payload:**
```json
{
  "studentId": "string"
}
```

**Response:**
```json
{
  "gpa": "number",
  "totalCredits": "number"
}
```

## 3. ĐĂNG KÝ GIẤY (TÀI LIỆU)

### API: `POST /api/crud/document-requests/create/`
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
  "id": "string"
}
```

### API: `GET /api/crud/document-requests/`
**Payload:** Không cần payload

**Response:**
```json
{
  "document_requests": [
    {
      "requestId": "string",
      "documentType": "string",
      "semester": "string",
      "requestDate": "string",
      "purpose": "string", 
      "status": "string"
    }
  ]
}
```

## 4. NHẬN THÔNG BÁO

### API: `GET /api/services/notifications/unread/`
**Payload:** Không cần payload

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
      "deliveredAt": "string"
    }
  ]
}
```

### API: `POST /api/services/notifications/{id}/mark-read/`
**Payload:** Không cần payload (chỉ cần notification ID trong URL)

**Response:**
```json
{
  "message": "Notification marked as read"
}
```

## 5. CẬP NHẬT THÔNG TIN CÁ NHÂN, ĐỔI MẬT KHẨU

### API: `PUT /api/crud/users/{id}/update/`
**Payload:**
```json
{
  "full_name": "string",
  "email": "string",
  "phone": "string",
  "address": "string"
}
```

**Response:**
```json
{
  "message": "User updated"
}
```

### API: `POST /api/auth/change-password/`
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

## 6. THEO DÕI TIẾN ĐỘ HỌC

### API: `GET /api/services/registration/available-courses/{student_id}/`
**Payload:** Không cần payload (student ID trong URL)

**Response:**
```json
{
  "courses": [
    {
      "courseClassId": "string",
      "courseCode": "string",
      "courseName": "string",
      "subject": "string",
      "credits": "number",
      "availableSlots": "number",
      "room": "string"
    }
  ]
}
```

### API: `POST /api/services/registration/check-prerequisites/`
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
      "subjectCode": "string",
      "subjectName": "string"
    }
  ]
}
```

### API: `GET /api/crud/tuition-fees/`
**Payload:** Không cần payload

**Response:**
```json
{
  "tuition_fees": [
    {
      "tuitionFeeId": "string",
      "student": "string",
      "semester": "string",
      "totalCredits": "number",
      "feePerCredit": "number",
      "totalAmount": "number",
      "paidAmount": "number",
      "paymentStatus": "string",
      "dueDate": "string"
    }
  ]
}
```

---

## THÔNG TIN CHUNG

**Base URL:** `http://127.0.0.1:8000/api/`

**Authentication:** Tất cả API yêu cầu Session Key trong header:
```
Authorization: Session {session_key}
X-Session-Key: {session_key}
```

**Đăng nhập Student:**
```
POST /api/auth/student/login/
{
  "username": "string",
  "password": "string"
}
```
