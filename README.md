# SƠ ĐỒ CHỨC NĂNG BFD MỨC 2
## HỆ THỐNG QUẢN LÝ ĐẠI HỌC

```
                    ┌─────────────────────────────────────┐
                    │     HỆ THỐNG QUẢN LÝ ĐẠI HỌC      │
                    │        (University Management)      │
                    └─────────────────┬───────────────────┘
                                      │
        ┌─────────────────────────────┼─────────────────────────────┐
        │                             │                             │
        ▼                             ▼                             ▼
┌───────────────┐            ┌───────────────┐            ┌───────────────┐
│  1. QUẢN LÝ   │            │  2. QUẢN LÝ   │            │  3. ĐĂNG KÝ   │
│   NGƯỜI DÙNG  │            │    HỌC VỤ     │            │   HỌC PHẦN    │
└───────┬───────┘            └───────┬───────┘            └───────┬───────┘
        │                            │                            │
   ┌────┼────┐                  ┌────┼────┐                  ┌────┼────┐
   ▼    ▼    ▼                  ▼    ▼    ▼                  ▼    ▼    ▼
┌─────┐┌─────┐┌─────┐        ┌─────┐┌─────┐┌─────┐        ┌─────┐┌─────┐┌─────┐
│1.1  ││1.2  ││1.3  │        │2.1  ││2.2  ││2.3  │        │3.1  ││3.2  ││3.3  │
│Sinh ││Giáo ││Xác  │        │Khoa ││Ngành││Môn  │        │Đăng ││Hủy  ││Xem  │
│viên ││viên ││thực │        │     ││học  ││học  │        │ký   ││đăng ││lịch │
└─────┘└─────┘└─────┘        └─────┘└─────┘└─────┘        │học  ││ký   ││học  │
                                     │     │               │phần ││     ││     │
                              ┌─────┐┌─────┐               └─────┘└─────┘└─────┘
                              │2.4  ││2.5  │                      │
                              │Lớp  ││Học  │               ┌─────┐▼
                              │học  ││kỳ   │               │3.4  │
                              └─────┘└─────┘               │Kiểm │
                                                          │tra  │
                                                          │tiên │
                                                          │quyết│
                                                          └─────┘

        ┌─────────────────────────────┼─────────────────────────────┐
        │                             │                             │
        ▼                             ▼                             ▼
┌───────────────┐            ┌───────────────┐            ┌───────────────┐
│  4. QUẢN LÝ   │            │  5. QUẢN LÝ   │            │  6. QUẢN LÝ   │
│   ĐIỂM SỐ     │            │   HỌC PHÍ     │            │   TÀI LIỆU    │
└───────┬───────┘            └───────┬───────┘            └───────┬───────┘
        │                            │                            │
   ┌────┼────┐                  ┌────┼────┐                  ┌────┼────┐
   ▼    ▼    ▼                  ▼    ▼    ▼                  ▼    ▼    ▼
┌─────┐┌─────┐┌─────┐        ┌─────┐┌─────┐┌─────┐        ┌─────┐┌─────┐┌─────┐
│4.1  ││4.2  ││4.3  │        │5.1  ││5.2  ││5.3  │        │6.1  ││6.2  ││6.3  │
│Nhập ││Cập  ││Xem  │        │Tính ││Thanh││Xem  │        │Yêu  ││Duyệt││Quản │
│điểm ││nhật ││điểm │        │học  ││toán ││lịch │        │cầu  ││yêu  ││lý   │
└─────┘└─────┘└─────┘        │phí  ││     ││sử   │        │tài  ││cầu  ││loại │
   │           │              └─────┘└─────┘└─────┘        │liệu ││     ││tài  │
┌─────┐    ┌─────┐                   │                    └─────┘└─────┘│liệu │
│4.4  │    │4.5  │            ┌─────┐▼                           │     └─────┘
│Tính │    │Xuất │            │5.4  │                     ┌─────┐▼
│GPA  │    │báo  │            │Quản │                     │6.4  │
│     │    │cáo  │            │lý   │                     │Theo │
└─────┘    └─────┘            │công │                     │dõi  │
                              │nợ   │                     │trạng│
                              └─────┘                     │thái │
                                                          └─────┘

        ┌─────────────────────────────┼─────────────────────────────┐
        │                             │                             │
        ▼                             ▼                             
┌───────────────┐            ┌───────────────┐            
│  7. QUẢN LÝ   │            │  8. BÁO CÁO   │            
│   THÔNG BÁO   │            │  & THỐNG KÊ   │            
└───────┬───────┘            └───────┬───────┘            
        │                            │                    
   ┌────┼────┐                  ┌────┼────┐               
   ▼    ▼    ▼                  ▼    ▼    ▼               
┌─────┐┌─────┐┌─────┐        ┌─────┐┌─────┐┌─────┐        
│7.1  ││7.2  ││7.3  │        │8.1  ││8.2  ││8.3  │        
│Tạo  ││Gửi  ││Xem  │        │Báo  ││Báo  ││Thống│        
│thông││thông││thông│        │cáo  ││cáo  ││kê   │        
│báo  ││báo  ││báo  │        │học  ││tài  ││đăng │        
└─────┘└─────┘└─────┘        │tập  ││chính││ký   │        
       │                     └─────┘└─────┘└─────┘        
┌─────┐▼                            │                     
│7.4  │                      ┌─────┐▼                     
│Quản │                      │8.4  │                      
│lý   │                      │Xuất │                      
│đối  │                      │báo  │                      
│tượng│                      │cáo  │                      
│nhận │                      └─────┘                      
└─────┘                                                   
```

## MÔ TẢ CHI TIẾT CÁC CHỨC NĂNG MỨC 2

### 1. QUẢN LÝ NGƯỜI DÙNG
- **1.1 Quản lý Sinh viên**: Thêm, sửa, xóa thông tin sinh viên
- **1.2 Quản lý Giáo viên**: Quản lý hồ sơ và thông tin giáo viên
- **1.3 Xác thực & Phân quyền**: Đăng nhập, phân quyền truy cập

### 2. QUẢN LÝ HỌC VỤ
- **2.1 Quản lý Khoa**: Quản lý các khoa trong trường
- **2.2 Quản lý Ngành học**: Quản lý các ngành đào tạo
- **2.3 Quản lý Môn học**: Quản lý danh sách môn học
- **2.4 Quản lý Lớp học**: Quản lý lớp học phần
- **2.5 Quản lý Học kỳ**: Quản lý thời gian học kỳ

### 3. ĐĂNG KÝ HỌC PHẦN
- **3.1 Đăng ký học phần**: Sinh viên đăng ký môn học
- **3.2 Hủy đăng ký**: Hủy đăng ký học phần
- **3.3 Xem lịch học**: Xem thời khóa biểu
- **3.4 Kiểm tra tiên quyết**: Kiểm tra điều kiện học trước

### 4. QUẢN LÝ ĐIỂM SỐ
- **4.1 Nhập điểm**: Giáo viên nhập điểm cho sinh viên
- **4.2 Cập nhật điểm**: Chỉnh sửa điểm số
- **4.3 Xem điểm**: Sinh viên xem điểm của mình
- **4.4 Tính GPA**: Tính điểm trung bình tích lũy
- **4.5 Xuất báo cáo điểm**: Tạo bảng điểm

### 5. QUẢN LÝ HỌC PHÍ
- **5.1 Tính học phí**: Tính toán học phí theo học phần
- **5.2 Thanh toán**: Xử lý thanh toán học phí
- **5.3 Xem lịch sử**: Theo dõi các giao dịch
- **5.4 Quản lý công nợ**: Quản lý nợ học phí

### 6. QUẢN LÝ TÀI LIỆU
- **6.1 Yêu cầu tài liệu**: Sinh viên yêu cầu giấy tờ
- **6.2 Duyệt yêu cầu**: Xử lý yêu cầu tài liệu
- **6.3 Quản lý loại tài liệu**: Quản lý các loại giấy tờ
- **6.4 Theo dõi trạng thái**: Theo dõi tiến độ xử lý

### 7. QUẢN LÝ THÔNG BÁO
- **7.1 Tạo thông báo**: Soạn thông báo mới
- **7.2 Gửi thông báo**: Phát thông báo đến người dùng
- **7.3 Xem thông báo**: Đọc thông báo đã nhận
- **7.4 Quản lý đối tượng nhận**: Chọn người nhận thông báo

### 8. BÁO CÁO & THỐNG KÊ
- **8.1 Báo cáo học tập**: Báo cáo kết quả học tập
- **8.2 Báo cáo tài chính**: Báo cáo thu chi học phí
- **8.3 Thống kê đăng ký**: Thống kê đăng ký học phần
- **8.4 Xuất báo cáo**: Tạo và xuất các loại báo cáo

## KIẾN TRÚC HỆ THỐNG
- **Backend**: Django REST API
- **Frontend**: React (Admin/Teacher: TypeScript, Student: JavaScript)
- **Database**: SQLite/PostgreSQL
