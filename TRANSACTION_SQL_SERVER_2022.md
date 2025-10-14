# TRANSACTION TRONG SQL SERVER 2022

## 1. CÁCH KHAI BÁO VÀ SỬ DỤNG TRANSACTION

### 1.1. BEGIN TRANSACTION

BEGIN TRANSACTION được sử dụng để bắt đầu một giao dịch mới. Cú pháp:

```sql
BEGIN TRANSACTION [transaction_name];
-- hoặc
BEGIN TRAN [transaction_name];
```

Ví dụ:

```sql
BEGIN TRANSACTION MyTransaction;
```

### 1.2. UPDATE trong Transaction

Sau khi bắt đầu transaction, các câu lệnh UPDATE sẽ được thực thi trong phạm vi giao dịch:

```sql
BEGIN TRANSACTION;

UPDATE Accounts 
SET Balance = Balance - 1000 
WHERE AccountID = 1;

UPDATE Accounts 
SET Balance = Balance + 1000 
WHERE AccountID = 2;
```

### 1.3. COMMIT TRANSACTION

COMMIT TRANSACTION được sử dụng để xác nhận và lưu vĩnh viễn tất cả các thay đổi trong giao dịch:

```sql
BEGIN TRANSACTION;

UPDATE Accounts 
SET Balance = Balance - 1000 
WHERE AccountID = 1;

UPDATE Accounts 
SET Balance = Balance + 1000 
WHERE AccountID = 2;

COMMIT TRANSACTION;
```

## 2. SỬ DỤNG ROLLBACK, SAVE TRANSACTION VÀ XEM LOG GIAO DỊCH

### 2.1. ROLLBACK TRANSACTION

ROLLBACK được sử dụng để hủy bỏ tất cả các thay đổi trong giao dịch và quay về trạng thái ban đầu:

```sql
BEGIN TRANSACTION;

UPDATE Accounts 
SET Balance = Balance - 1000 
WHERE AccountID = 1;

-- Kiểm tra điều kiện
IF (SELECT Balance FROM Accounts WHERE AccountID = 1) < 0
BEGIN
    ROLLBACK TRANSACTION;
    PRINT 'Transaction rolled back: Insufficient balance';
END
ELSE
BEGIN
    UPDATE Accounts 
    SET Balance = Balance + 1000 
    WHERE AccountID = 2;
    
    COMMIT TRANSACTION;
    PRINT 'Transaction committed successfully';
END
```

### 2.2. SAVE TRANSACTION (Savepoint)

SAVE TRANSACTION tạo một điểm lưu trong giao dịch, cho phép rollback về điểm cụ thể thay vì rollback toàn bộ:

Cấu trúc table cho ví dụ:
```
TransactionLog (LogID, AccountID, TransactionType, Amount, TransactionDate)
Accounts (AccountID, AccountName, Balance, Status)
```

```sql
BEGIN TRANSACTION MainTransaction;

-- Bước 1: Trừ tiền tài khoản nguồn
UPDATE Accounts 
SET Balance = Balance - 5000 
WHERE AccountID = 1;

INSERT INTO TransactionLog (AccountID, TransactionType, Amount, TransactionDate)
VALUES (1, 'DEBIT', 5000, GETDATE());

-- Tạo savepoint sau bước 1
SAVE TRANSACTION SavePoint1;

-- Bước 2: Cộng tiền tài khoản đích
UPDATE Accounts 
SET Balance = Balance + 5000 
WHERE AccountID = 2;

INSERT INTO TransactionLog (AccountID, TransactionType, Amount, TransactionDate)
VALUES (2, 'CREDIT', 5000, GETDATE());

-- Tạo savepoint sau bước 2
SAVE TRANSACTION SavePoint2;

-- Bước 3: Cập nhật trạng thái
UPDATE Accounts 
SET Status = 'ACTIVE' 
WHERE AccountID IN (1, 2);

-- Nếu có lỗi ở bước 3, rollback về SavePoint2
IF @@ERROR <> 0
BEGIN
    ROLLBACK TRANSACTION SavePoint2;
    PRINT 'Rolled back to SavePoint2';
END
ELSE
BEGIN
    COMMIT TRANSACTION;
    PRINT 'All changes committed';
END
```

### 2.3. Xem Log Giao Dịch

SQL Server lưu trữ thông tin giao dịch trong transaction log. Để xem log:

```sql
-- Xem thông tin transaction log file
SELECT 
    name AS LogFileName,
    physical_name AS PhysicalLocation,
    size * 8 / 1024 AS SizeMB,
    max_size * 8 / 1024 AS MaxSizeMB
FROM sys.database_files
WHERE type_desc = 'LOG';

-- Xem các transaction đang hoạt động
SELECT 
    transaction_id,
    name,
    transaction_begin_time,
    transaction_type,
    transaction_state
FROM sys.dm_tran_active_transactions;

-- Xem session đang có transaction
SELECT 
    s.session_id,
    s.login_name,
    t.transaction_id,
    t.name AS transaction_name,
    t.transaction_begin_time,
    CASE t.transaction_state
        WHEN 0 THEN 'Uninitialized'
        WHEN 1 THEN 'Initialized'
        WHEN 2 THEN 'Active'
        WHEN 3 THEN 'Ended'
        WHEN 4 THEN 'Commit started'
        WHEN 5 THEN 'Prepared'
        WHEN 6 THEN 'Committed'
        WHEN 7 THEN 'Rolling back'
        WHEN 8 THEN 'Rolled back'
    END AS transaction_state
FROM sys.dm_tran_session_transactions st
INNER JOIN sys.dm_tran_active_transactions t 
    ON st.transaction_id = t.transaction_id
INNER JOIN sys.dm_exec_sessions s 
    ON st.session_id = s.session_id;

-- Xem log space usage
DBCC SQLPERF(LOGSPACE);

-- Xem transaction log records
SELECT 
    [Current LSN],
    [Operation],
    [Context],
    [Transaction ID],
    [Transaction Name],
    [Begin Time]
FROM fn_dblog(NULL, NULL)
WHERE [Transaction Name] IS NOT NULL
ORDER BY [Begin Time] DESC;
```

## 3. MÔ PHỎNG TÌNH HUỐNG THỰC TẾ: CHUYỂN TIỀN GIỮA HAI TÀI KHOẢN

### 3.1. Cấu trúc Tables

```sql
-- Bảng Customers
Customers (
    CustomerID INT PRIMARY KEY,
    CustomerName NVARCHAR(100),
    Email NVARCHAR(100),
    Phone NVARCHAR(20),
    Address NVARCHAR(200),
    CreatedDate DATETIME
)

-- Bảng Accounts
Accounts (
    AccountID INT PRIMARY KEY,
    CustomerID INT FOREIGN KEY REFERENCES Customers(CustomerID),
    AccountNumber NVARCHAR(20),
    AccountType NVARCHAR(50),
    Balance DECIMAL(18,2),
    Status NVARCHAR(20),
    CreatedDate DATETIME,
    LastModified DATETIME
)

-- Bảng TransactionHistory
TransactionHistory (
    TransactionID INT PRIMARY KEY IDENTITY,
    FromAccountID INT,
    ToAccountID INT,
    Amount DECIMAL(18,2),
    TransactionType NVARCHAR(50),
    TransactionDate DATETIME,
    Status NVARCHAR(20),
    Description NVARCHAR(500),
    ReferenceNumber NVARCHAR(50)
)

-- Bảng AuditLog
AuditLog (
    AuditID INT PRIMARY KEY IDENTITY,
    TableName NVARCHAR(100),
    Operation NVARCHAR(50),
    OldValue NVARCHAR(MAX),
    NewValue NVARCHAR(MAX),
    ModifiedBy NVARCHAR(100),
    ModifiedDate DATETIME
)
```

### 3.2. Tạo Tables và Insert Dữ Liệu Mẫu

```sql
-- Tạo database
CREATE DATABASE BankingSystem;
GO

USE BankingSystem;
GO

-- Tạo bảng Customers
CREATE TABLE Customers (
    CustomerID INT PRIMARY KEY,
    CustomerName NVARCHAR(100) NOT NULL,
    Email NVARCHAR(100),
    Phone NVARCHAR(20),
    Address NVARCHAR(200),
    CreatedDate DATETIME DEFAULT GETDATE()
);

-- Tạo bảng Accounts
CREATE TABLE Accounts (
    AccountID INT PRIMARY KEY,
    CustomerID INT FOREIGN KEY REFERENCES Customers(CustomerID),
    AccountNumber NVARCHAR(20) UNIQUE NOT NULL,
    AccountType NVARCHAR(50) NOT NULL,
    Balance DECIMAL(18,2) NOT NULL DEFAULT 0,
    Status NVARCHAR(20) NOT NULL DEFAULT 'ACTIVE',
    CreatedDate DATETIME DEFAULT GETDATE(),
    LastModified DATETIME DEFAULT GETDATE(),
    CONSTRAINT CHK_Balance CHECK (Balance >= 0)
);

-- Tạo bảng TransactionHistory
CREATE TABLE TransactionHistory (
    TransactionID INT PRIMARY KEY IDENTITY(1,1),
    FromAccountID INT,
    ToAccountID INT,
    Amount DECIMAL(18,2) NOT NULL,
    TransactionType NVARCHAR(50) NOT NULL,
    TransactionDate DATETIME DEFAULT GETDATE(),
    Status NVARCHAR(20) NOT NULL,
    Description NVARCHAR(500),
    ReferenceNumber NVARCHAR(50) UNIQUE
);

-- Tạo bảng AuditLog
CREATE TABLE AuditLog (
    AuditID INT PRIMARY KEY IDENTITY(1,1),
    TableName NVARCHAR(100) NOT NULL,
    Operation NVARCHAR(50) NOT NULL,
    OldValue NVARCHAR(MAX),
    NewValue NVARCHAR(MAX),
    ModifiedBy NVARCHAR(100) DEFAULT SYSTEM_USER,
    ModifiedDate DATETIME DEFAULT GETDATE()
);

-- Insert dữ liệu mẫu
INSERT INTO Customers (CustomerID, CustomerName, Email, Phone, Address)
VALUES 
(1, N'Nguyễn Văn An', 'nguyenvanan@email.com', '0901234567', N'123 Lê Lợi, Q1, TP.HCM'),
(2, N'Trần Thị Bình', 'tranthibinh@email.com', '0902345678', N'456 Nguyễn Huệ, Q1, TP.HCM'),
(3, N'Lê Văn Cường', 'levancuong@email.com', '0903456789', N'789 Trần Hưng Đạo, Q5, TP.HCM');

INSERT INTO Accounts (AccountID, CustomerID, AccountNumber, AccountType, Balance, Status)
VALUES 
(1, 1, 'ACC001', 'SAVINGS', 10000000.00, 'ACTIVE'),
(2, 2, 'ACC002', 'CHECKING', 5000000.00, 'ACTIVE'),
(3, 3, 'ACC003', 'SAVINGS', 15000000.00, 'ACTIVE');
```

### 3.3. Demo Kết Quả TRƯỚC khi Transaction

```sql
-- Xem số dư trước khi chuyển tiền
SELECT 
    A.AccountID,
    A.AccountNumber,
    C.CustomerName,
    A.Balance,
    A.Status
FROM Accounts A
INNER JOIN Customers C ON A.CustomerID = C.CustomerID
WHERE A.AccountID IN (1, 2);

/*
Kết quả:
AccountID | AccountNumber | CustomerName      | Balance      | Status
----------|---------------|-------------------|--------------|--------
1         | ACC001        | Nguyễn Văn An     | 10000000.00  | ACTIVE
2         | ACC002        | Trần Thị Bình     | 5000000.00   | ACTIVE
*/

-- Xem lịch sử giao dịch
SELECT * FROM TransactionHistory;
-- Kết quả: (0 rows) - Chưa có giao dịch nào
```
