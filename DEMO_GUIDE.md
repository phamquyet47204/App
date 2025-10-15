# Hướng Dẫn Demo - Transaction trong SQL Server 2022

## 🎯 Tóm Tắt Nội Dung Demo

### 1. Các Lệnh Transaction Cơ Bản
- **BEGIN TRANSACTION** - Bắt đầu giao dịch
- **UPDATE** - Cập nhật dữ liệu trong transaction
- **COMMIT TRANSACTION** - Xác nhận thay đổi
- **ROLLBACK** - Hoàn tác giao dịch
- **SAVE TRANSACTION** - Tạo savepoint
- **Xem log giao dịch** - Theo dõi transaction log

### 2. Demo Chuyển Tiền (Tình Huống Thực Tế)
```sql
-- Tạo bảng tài khoản
CREATE TABLE Accounts (
    AccountID INT PRIMARY KEY,
    Balance DECIMAL(10,2)
);

-- Chèn dữ liệu mẫu
INSERT INTO Accounts VALUES (1, 1000.00), (2, 500.00);

-- TRƯỚC khi chuyển tiền
SELECT * FROM Accounts;

-- Transaction chuyển tiền (đảm bảo tính nguyên tử)
BEGIN TRANSACTION;
    UPDATE Accounts SET Balance = Balance - 200 WHERE AccountID = 1;
    UPDATE Accounts SET Balance = Balance + 200 WHERE AccountID = 2;
COMMIT TRANSACTION;

-- SAU khi chuyển tiền
SELECT * FROM Accounts;
```

### 3. Demo ROLLBACK và SAVE TRANSACTION
```sql
BEGIN TRANSACTION;
    UPDATE Accounts SET Balance = Balance - 100 WHERE AccountID = 1;
    SAVE TRANSACTION SavePoint1;
    UPDATE Accounts SET Balance = Balance + 100 WHERE AccountID = 2;
    -- Rollback về savepoint
    ROLLBACK TRANSACTION SavePoint1;
COMMIT TRANSACTION;
```

### 4. Xem Transaction Log
```sql
-- Xem log giao dịch
SELECT * FROM sys.fn_dblog(NULL, NULL);
```

### 5. Tính Năng Mới SQL Server 2022
- **Accelerated Database Recovery (ADR)** - Phục hồi nhanh hơn
- **Intelligent Query Processing** - Tối ưu hóa transaction
- **Memory-Optimized TempDB** - Cải thiện hiệu suất
- **Enhanced Transaction Log** - Log management tốt hơn

## 🚀 Các Bước Demo Chi Tiết

### Bước 1: Chuẩn Bị Database
```sql
CREATE DATABASE TransactionDemo;
USE TransactionDemo;
```

### Bước 2: Demo Transaction Cơ Bản
1. Tạo bảng và dữ liệu mẫu
2. Thực hiện BEGIN TRANSACTION
3. Thực hiện UPDATE
4. Demo COMMIT và ROLLBACK

### Bước 3: Demo Chuyển Tiền
1. Hiển thị dữ liệu TRƯỚC transaction
2. Thực hiện transaction chuyển tiền
3. Hiển thị dữ liệu SAU transaction
4. Chứng minh tính nguyên tử (ACID)

### Bước 4: Demo SAVE TRANSACTION
1. Tạo savepoint trong transaction
2. Thực hiện rollback về savepoint
3. So sánh kết quả

### Bước 5: Xem Transaction Log
1. Kiểm tra log entries
2. Phân tích transaction history

## ⚡ Script Demo Hoàn Chỉnh
```sql
-- Setup
CREATE DATABASE TransactionDemo;
USE TransactionDemo;
CREATE TABLE Accounts (AccountID INT PRIMARY KEY, Balance DECIMAL(10,2));
INSERT INTO Accounts VALUES (1, 1000.00), (2, 500.00);

-- Demo chuyển tiền
SELECT 'TRƯỚC' AS Status, * FROM Accounts;
BEGIN TRANSACTION;
    UPDATE Accounts SET Balance = Balance - 200 WHERE AccountID = 1;
    UPDATE Accounts SET Balance = Balance + 200 WHERE AccountID = 2;
COMMIT TRANSACTION;
SELECT 'SAU' AS Status, * FROM Accounts;
```

## 📝 Điểm Nhấn Demo
- Tính nguyên tử của transaction
- Sự khác biệt COMMIT vs ROLLBACK
- Ứng dụng thực tế trong chuyển tiền
- Tính năng mới SQL Server 2022

## 🔗 Tài Liệu Tham Khảo
- [Phần 1: Cơ bản](./TRANSACTION_SQL_SERVER_2022.md)
- [Phần 2: Nâng cao](./TRANSACTION_SQL_SERVER_2022_Part2.md)
- [Phần 3: Tối ưu hóa](./TRANSACTION_SQL_SERVER_2022_Part3.md)
- [Phần 4: Thực tế](./TRANSACTION_SQL_SERVER_2022_Part4.md)