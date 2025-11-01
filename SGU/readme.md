# 🎓 Student Management System - Frontend

Dự án giao diện người dùng (frontend) cho hệ thống **Quản lý Sinh viên**, được phát triển bằng **React + Vite**.

---

## 🚀 Hướng Dẫn Chạy Dự Án

Thực hiện các bước sau để chạy dự án trên máy của bạn:

### Di chuyển vào thư mục gốc của dự án
```bash
cd ten-thu-muc-du-an

**chạy:** `npm i`
**sau đó chạy:** `npm run dev`

---
# 📋 Danh Sách API (Lỗi hoặc Cần Kiểm Tra)

Dưới đây là danh sách các API hiện tại có vấn đề hoặc cần được xác minh trong hệ thống.

---

### 🔔 Xem tất cả thông báo  
**Lỗi:** `500`
**Phương thức:** `GET`  
**Endpoint:** `/student/my-document-requests/`
---

###  Kiểm tra tiên quyết
**Lỗi:** `400`
**Phương thức:** `POST`  
**Endpoint:** `/api/services/registration/check-prerequisites/`

---
###  Kiểm tra lịch
**Lỗi:** `400`
**Phương thức:** `POST`  
**Endpoint:** `/api/services/registration/check-schedule-conflict/`

---
###  Đăng ký môn học
**Lỗi:** `400`
**Phương thức:** `POST`  
**Endpoint:** `crud/registrations/create/`

---
### cập nhật thông tin cá nhân
**không thay đổi được mail, mặc dù payload đã truyền lên server **