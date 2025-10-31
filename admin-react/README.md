# Admin Dashboard - University Management System

Giao diện quản trị cho hệ thống quản lý trường đại học.

## 🚀 Khởi chạy

```bash
cd admin-react
npm start
```

Ứng dụng sẽ chạy tại: http://localhost:3000

## 📋 Tính năng

### ✅ Đã hoàn thành:
- **Dashboard**: Tổng quan thống kê
- **Sidebar Navigation**: Menu điều hướng với các chức năng
- **Authentication**: Đăng nhập admin
- **Departments**: Quản lý khoa (CRUD)
- **Majors**: Quản lý ngành học (CRUD) 
- **Subjects**: Quản lý môn học (CRUD)
- **Reports**: Giao diện báo cáo

### 🔄 Đang phát triển:
- Students Management
- Teachers Management  
- Grades Management
- Advanced Reports

## 🎨 Giao diện

- **Responsive Design**: Tương thích mobile/desktop
- **Modern UI**: Sử dụng Lucide React icons
- **Clean Layout**: Sidebar + Main content
- **Professional Styling**: CSS hiện đại

## 🔧 Công nghệ

- **React 18** + **TypeScript**
- **React Router** cho navigation
- **Axios** cho API calls
- **Lucide React** cho icons

## 📡 API Integration

Kết nối với Django backend tại `http://127.0.0.1:8000/api/`

### Endpoints đã tích hợp:
- `/auth/admin/login/` - Đăng nhập
- `/admin/dashboard/` - Dashboard stats
- `/crud/departments/` - CRUD Khoa
- `/crud/majors/` - CRUD Ngành học
- `/crud/subjects/` - CRUD Môn học

## 🔐 Authentication

Sử dụng session-based authentication với Django backend.

**Tài khoản test:**
- master / master123
- admin / python123

## 📁 Cấu trúc thư mục

```
src/
├── components/
│   ├── Layout.tsx
│   └── Sidebar.tsx
├── pages/
│   ├── Dashboard.tsx
│   ├── Login.tsx
│   ├── Departments.tsx
│   ├── Majors.tsx
│   ├── Subjects.tsx
│   ├── Students.tsx
│   ├── Teachers.tsx
│   ├── Grades.tsx
│   └── Reports.tsx
├── services/
│   └── api.ts
├── App.tsx
└── App.css
```

## 🎯 Hướng dẫn sử dụng

1. **Khởi động Django backend** trước
2. **Đăng nhập** với tài khoản admin
3. **Điều hướng** qua sidebar menu
4. **Quản lý dữ liệu** qua các trang CRUD

## 🔮 Roadmap

- [ ] Hoàn thiện CRUD cho Students/Teachers
- [ ] Thêm form tạo/sửa cho các entities
- [ ] Tích hợp Grade management
- [ ] Advanced filtering & search
- [ ] Export/Import Excel
- [ ] Real-time notifications
- [ ] Dark mode theme