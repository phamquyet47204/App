# TRANSACTION TRONG SQL SERVER 2022 - BẢN RÚT GỌN

## 1. CÁCH KHAI BÁO VÀ SỬ DỤNG TRANSACTION

### 1.1. Cú Pháp Cơ Bản

```sql
-- Bắt đầu transaction
BEGIN TRANSACTION [tên_transaction];

-- Thực hiện các câu lệnh UPDATE
UPDATE table_name SET column = value WHERE condition;

-- Xác nhận thay đổi
COMMIT TRANSACTION;

-- Hoặc hủy bỏ thay đổi
ROLLBACK TRANSACTION;
```

### 1.2. Ví Dụ Đơn Giản

```sql
BEGIN TRANSACTION;

UPDATE Accounts 
SET Balance = Balance - 1000000 
WHERE AccountID = 1;

UPDATE Accounts 
SET Balance = Balance + 1000000 
WHERE AccountID = 2;

COMMIT TRANSACTION;
```

## 2. SỬ DỤNG ROLLBACK, SAVE TRANSACTION VÀ XEM LOG

### 2.1. ROLLBACK với Điều Kiện

```sql
BEGIN TRANSACTION;

UPDATE Accounts 
SET Balance = Balance - 1000000 
WHERE AccountID = 1;

-- Kiểm tra điều kiện
IF (SELECT Balance FROM Accounts WHERE AccountID = 1) < 0
BEGIN
    ROLLBACK TRANSACTION;
    PRINT N'Giao dịch bị hủy: Số dư không đủ';
END
ELSE
BEGIN
    UPDATE Accounts 
    SET Balance = Balance + 1000000 
    WHERE AccountID = 2;
    
    COMMIT TRANSACTION;
    PRINT N'Giao dịch thành công';
END
```

### 2.2. SAVE TRANSACTION (Savepoint)

```sql
BEGIN TRANSACTION MainTransaction;

-- Bước 1: Trừ tiền
UPDATE Accounts SET Balance = Balance - 5000000 WHERE AccountID = 1;
SAVE TRANSACTION SavePoint1;

-- Bước 2: Cộng tiền
UPDATE Accounts SET Balance = Balance + 5000000 WHERE AccountID = 2;
SAVE TRANSACTION SavePoint2;

-- Bước 3: Cập nhật trạng thái
UPDATE Accounts SET Status = 'ACTIVE' WHERE AccountID IN (1, 2);

-- Nếu có lỗi ở bước 3, rollback về SavePoint2
IF @@ERROR <> 0
BEGIN
    ROLLBACK TRANSACTION SavePoint2;
    PRINT N'Rollback về SavePoint2';
END
ELSE
BEGIN
    COMMIT TRANSACTION;
    PRINT N'Tất cả thay đổi đã được commit';
END
```

### 2.3. Xem Log Giao Dịch

```sql
-- Xem các transaction đang hoạt động
SELECT 
    transaction_id,
    name,
    transaction_begin_time,
    transaction_state
FROM sys.dm_tran_active_transactions;

-- Xem session có transaction
SELECT 
    s.session_id,
    s.login_name,
    t.transaction_id,
    t.name AS transaction_name,
    CASE t.transaction_state
        WHEN 2 THEN 'Active'
        WHEN 6 THEN 'Committed'
        WHEN 7 THEN 'Rolling back'
        WHEN 8 THEN 'Rolled back'
    END AS transaction_state
FROM sys.dm_tran_session_transactions st
INNER JOIN sys.dm_tran_active_transactions t ON st.transaction_id = t.transaction_id
INNER JOIN sys.dm_exec_sessions s ON st.session_id = s.session_id;

-- Xem log space usage
DBCC SQLPERF(LOGSPACE);
```

## 3. MÔ PHỎNG TÌNH HUỐNG THỰC TẾ: CHUYỂN TIỀN

### 3.1. Tạo Cấu Trúc Database

```sql
-- Tạo database
CREATE DATABASE BankingSystem;
USE BankingSystem;

-- Bảng Customers
CREATE TABLE Customers (
    CustomerID INT PRIMARY KEY,
    CustomerName NVARCHAR(100) NOT NULL,
    Email NVARCHAR(100),
    CreatedDate DATETIME DEFAULT GETDATE()
);

-- Bảng Accounts
CREATE TABLE Accounts (
    AccountID INT PRIMARY KEY,
    CustomerID INT FOREIGN KEY REFERENCES Customers(CustomerID),
    AccountNumber NVARCHAR(20) UNIQUE NOT NULL,
    Balance DECIMAL(18,2) NOT NULL DEFAULT 0,
    Status NVARCHAR(20) NOT NULL DEFAULT 'ACTIVE',
    LastModified DATETIME DEFAULT GETDATE(),
    CONSTRAINT CHK_Balance CHECK (Balance >= 0)
);

-- Bảng TransactionHistory
CREATE TABLE TransactionHistory (
    TransactionID INT PRIMARY KEY IDENTITY(1,1),
    FromAccountID INT,
    ToAccountID INT,
    Amount DECIMAL(18,2) NOT NULL,
    TransactionType NVARCHAR(50) NOT NULL,
    TransactionDate DATETIME DEFAULT GETDATE(),
    Status NVARCHAR(20) NOT NULL,
    ReferenceNumber NVARCHAR(50) UNIQUE
);

-- Insert dữ liệu mẫu
INSERT INTO Customers (CustomerID, CustomerName, Email)
VALUES 
(1, N'Nguyễn Văn An', 'nguyenvanan@email.com'),
(2, N'Trần Thị Bình', 'tranthibinh@email.com');

INSERT INTO Accounts (AccountID, CustomerID, AccountNumber, Balance, Status)
VALUES 
(1, 1, 'ACC001', 10000000.00, 'ACTIVE'),
(2, 2, 'ACC002', 5000000.00, 'ACTIVE');
```

### 3.2. Demo TRƯỚC khi Transaction

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
Kết quả TRƯỚC:
AccountID | AccountNumber | CustomerName      | Balance      | Status
----------|---------------|-------------------|--------------|--------
1         | ACC001        | Nguyễn Văn An     | 10000000.00  | ACTIVE
2         | ACC002        | Trần Thị Bình     | 5000000.00   | ACTIVE
*/
```

### 3.3. Stored Procedure Chuyển Tiền

```sql
CREATE PROCEDURE sp_TransferMoney
    @FromAccountID INT,
    @ToAccountID INT,
    @Amount DECIMAL(18,2),
    @Description NVARCHAR(500)
AS
BEGIN
    SET NOCOUNT ON;
    
    DECLARE @FromBalance DECIMAL(18,2);
    DECLARE @ReferenceNumber NVARCHAR(50);
    
    -- Tạo reference number
    SET @ReferenceNumber = 'TXN' + FORMAT(GETDATE(), 'yyyyMMddHHmmss');
    
    BEGIN TRY
        BEGIN TRANSACTION TransferMoney;
        
        -- Kiểm tra tài khoản nguồn
        IF NOT EXISTS (SELECT 1 FROM Accounts WHERE AccountID = @FromAccountID AND Status = 'ACTIVE')
        BEGIN
            THROW 50001, N'Tài khoản nguồn không hợp lệ', 1;
        END
        
        -- Kiểm tra tài khoản đích
        IF NOT EXISTS (SELECT 1 FROM Accounts WHERE AccountID = @ToAccountID AND Status = 'ACTIVE')
        BEGIN
            THROW 50002, N'Tài khoản đích không hợp lệ', 1;
        END
        
        -- Kiểm tra số tiền
        IF @Amount <= 0
        BEGIN
            THROW 50003, N'Số tiền phải lớn hơn 0', 1;
        END
        
        -- Lấy số dư và kiểm tra
        SELECT @FromBalance = Balance 
        FROM Accounts WITH (UPDLOCK, HOLDLOCK)
        WHERE AccountID = @FromAccountID;
        
        IF @FromBalance < @Amount
        BEGIN
            THROW 50004, N'Số dư không đủ', 1;
        END
        
        -- Trừ tiền từ tài khoản nguồn
        UPDATE Accounts
        SET Balance = Balance - @Amount,
            LastModified = GETDATE()
        WHERE AccountID = @FromAccountID;
        
        -- Cộng tiền vào tài khoản đích
        UPDATE Accounts
        SET Balance = Balance + @Amount,
            LastModified = GETDATE()
        WHERE AccountID = @ToAccountID;
        
        -- Ghi lịch sử giao dịch
        INSERT INTO TransactionHistory (
            FromAccountID, ToAccountID, Amount, TransactionType, 
            Status, Description, ReferenceNumber
        )
        VALUES (
            @FromAccountID, @ToAccountID, @Amount, 'TRANSFER',
            'COMPLETED', @Description, @ReferenceNumber
        );
        
        COMMIT TRANSACTION TransferMoney;
        
        PRINT N'Giao dịch thành công! Mã: ' + @ReferenceNumber;
        
    END TRY
    BEGIN CATCH
        IF @@TRANCOUNT > 0
            ROLLBACK TRANSACTION TransferMoney;
        
        PRINT N'Giao dịch thất bại: ' + ERROR_MESSAGE();
        THROW;
    END CATCH
END;
```

### 3.4. Thực Hiện Giao Dịch

```sql
-- Chuyển 2,000,000 VND từ tài khoản 1 sang tài khoản 2
EXEC sp_TransferMoney 
    @FromAccountID = 1,
    @ToAccountID = 2,
    @Amount = 2000000.00,
    @Description = N'Chuyển tiền thanh toán';

-- Kết quả: Giao dịch thành công! Mã: TXN20241215143025
```

### 3.5. Demo SAU khi Transaction

```sql
-- Xem số dư sau khi chuyển tiền
SELECT 
    A.AccountID,
    A.AccountNumber,
    C.CustomerName,
    A.Balance,
    A.Status,
    A.LastModified
FROM Accounts A
INNER JOIN Customers C ON A.CustomerID = C.CustomerID
WHERE A.AccountID IN (1, 2);

/*
Kết quả SAU:
AccountID | AccountNumber | CustomerName      | Balance      | Status | LastModified
----------|---------------|-------------------|--------------|--------|------------------
1         | ACC001        | Nguyễn Văn An     | 8000000.00   | ACTIVE | 2024-12-15 14:30:25
2         | ACC002        | Trần Thị Bình     | 7000000.00   | ACTIVE | 2024-12-15 14:30:25

Giải thích:
- Tài khoản 1: 10,000,000 - 2,000,000 = 8,000,000 VND
- Tài khoản 2: 5,000,000 + 2,000,000 = 7,000,000 VND
*/

-- Xem lịch sử giao dịch
SELECT 
    TransactionID,
    FromAccountID,
    ToAccountID,
    Amount,
    TransactionDate,
    Status,
    ReferenceNumber
FROM TransactionHistory
ORDER BY TransactionDate DESC;

/*
Kết quả:
TransactionID | FromAccountID | ToAccountID | Amount      | TransactionDate      | Status    | ReferenceNumber
--------------|---------------|-------------|-------------|----------------------|-----------|------------------
1             | 1             | 2           | 2000000.00  | 2024-12-15 14:30:25  | COMPLETED | TXN20241215143025
*/
```

### 3.6. Demo Giao Dịch Thất Bại

```sql
-- Thử chuyển 15,000,000 VND (vượt số dư)
EXEC sp_TransferMoney 
    @FromAccountID = 1,
    @ToAccountID = 2,
    @Amount = 15000000.00,
    @Description = N'Chuyển tiền mua nhà';

-- Kết quả: Giao dịch thất bại: Số dư không đủ

-- Kiểm tra số dư không thay đổi
SELECT AccountID, Balance FROM Accounts WHERE AccountID = 1;
-- Kết quả: AccountID=1, Balance=8000000.00 (không đổi)
```

## 4. TÍNH NĂNG MỚI TRONG SQL SERVER 2022

### 4.1. Accelerated Database Recovery (ADR)

```sql
-- Bật ADR cho recovery nhanh hơn
ALTER DATABASE BankingSystem SET ACCELERATED_DATABASE_RECOVERY = ON;

-- Kiểm tra trạng thái ADR
SELECT 
    name AS DatabaseName,
    is_accelerated_database_recovery_on AS ADR_Enabled
FROM sys.databases
WHERE name = 'BankingSystem';

/*
Lợi ích ADR:
- Recovery nhanh hơn sau crash
- Rollback transaction dài nhanh hơn
- Giảm thời gian downtime
*/
```

### 4.2. Ledger Tables - Tính Năng Mới

```sql
-- Tạo Ledger Table đảm bảo tính toàn vẹn
CREATE TABLE LedgerAccounts (
    AccountID INT NOT NULL,
    AccountNumber NVARCHAR(20) NOT NULL,
    Balance DECIMAL(18,2) NOT NULL,
    LastModified DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME()
)
WITH (
    LEDGER = ON (
        LEDGER_VIEW = LedgerAccountsView
    )
);

-- Thực hiện transaction với Ledger
BEGIN TRANSACTION;

INSERT INTO LedgerAccounts (AccountID, AccountNumber, Balance)
VALUES (1, 'LED001', 10000000.00);

UPDATE LedgerAccounts 
SET Balance = Balance - 1000000.00
WHERE AccountID = 1;

COMMIT TRANSACTION;

-- Xem ledger history (không thể xóa/sửa)
SELECT 
    AccountID,
    Balance,
    ledger_transaction_id,
    ledger_operation_type_desc
FROM LedgerAccountsView
ORDER BY ledger_sequence_number;

-- Verify tính toàn vẹn
EXEC sp_verify_database_ledger;
```

### 4.3. Intelligent Query Processing

```sql
-- Bật tính năng mới SQL Server 2022
ALTER DATABASE BankingSystem SET COMPATIBILITY_LEVEL = 160;

-- Parameter Sensitive Plan Optimization
CREATE PROCEDURE sp_GetTransactionHistory
    @AccountID INT,
    @Days INT
AS
BEGIN
    SELECT 
        TransactionID,
        Amount,
        TransactionDate
    FROM TransactionHistory
    WHERE FromAccountID = @AccountID
        AND TransactionDate >= DATEADD(DAY, -@Days, GETDATE())
    OPTION (USE HINT('PARAMETER_SENSITIVE_PLAN_OPTIMIZATION'));
END;

-- SQL Server 2022 tự động tạo plan khác nhau cho parameter khác nhau
EXEC sp_GetTransactionHistory @AccountID = 1, @Days = 7;   -- Plan cho ít data
EXEC sp_GetTransactionHistory @AccountID = 1, @Days = 365; -- Plan cho nhiều data
```

### 4.4. JSON Support Cải Tiến

```sql
-- Transaction với JSON metadata
CREATE TABLE TransactionMetadata (
    TransactionID INT PRIMARY KEY IDENTITY,
    MetadataJSON NVARCHAR(MAX),
    CONSTRAINT CK_JSON CHECK (ISJSON(MetadataJSON) = 1)
);

BEGIN TRANSACTION;

DECLARE @JsonData NVARCHAR(MAX) = N'{
    "transactionType": "TRANSFER",
    "amount": 2000000.00,
    "fromAccount": {"id": 1, "number": "ACC001"},
    "toAccount": {"id": 2, "number": "ACC002"},
    "deviceInfo": {"type": "mobile", "os": "iOS"}
}';

INSERT INTO TransactionMetadata (MetadataJSON) VALUES (@JsonData);

-- Query JSON data
SELECT 
    JSON_VALUE(MetadataJSON, '$.transactionType') AS Type,
    JSON_VALUE(MetadataJSON, '$.amount') AS Amount,
    JSON_VALUE(MetadataJSON, '$.deviceInfo.type') AS Device
FROM TransactionMetadata;

COMMIT TRANSACTION;
```

### 4.5. Time Series Functions

```sql
-- Phân tích transaction theo thời gian với DATE_BUCKET
SELECT 
    DATE_BUCKET(HOUR, 1, TransactionDate) AS TimeWindow,
    COUNT(*) AS TransactionCount,
    SUM(Amount) AS TotalAmount
FROM TransactionHistory
WHERE TransactionDate >= DATEADD(DAY, -7, GETDATE())
GROUP BY DATE_BUCKET(HOUR, 1, TransactionDate)
ORDER BY TimeWindow;

-- Tạo time series với GENERATE_SERIES
SELECT 
    value AS HourOfDay,
    ISNULL(T.TransactionCount, 0) AS TransactionCount
FROM GENERATE_SERIES(0, 23, 1) AS Hours
LEFT JOIN (
    SELECT 
        DATEPART(HOUR, TransactionDate) AS Hour,
        COUNT(*) AS TransactionCount
    FROM TransactionHistory
    WHERE CAST(TransactionDate AS DATE) = CAST(GETDATE() AS DATE)
    GROUP BY DATEPART(HOUR, TransactionDate)
) T ON Hours.value = T.Hour
ORDER BY Hours.value;
```

### 4.6. Improved Deadlock Detection

```sql
-- Bật monitoring deadlock
CREATE EVENT SESSION DeadlockMonitor ON SERVER
ADD EVENT sqlserver.database_xml_deadlock_report
ADD TARGET package0.event_file(SET filename=N'C:\Logs\Deadlocks.xel');

ALTER EVENT SESSION DeadlockMonitor ON SERVER STATE = START;

-- SQL Server 2022 phát hiện và xử lý deadlock nhanh hơn
```

## KẾT LUẬN

**Các điểm chính về Transaction trong SQL Server 2022:**

1. **Cú pháp cơ bản**: BEGIN TRANSACTION → UPDATE → COMMIT/ROLLBACK
2. **ROLLBACK**: Hủy bỏ thay đổi khi có lỗi
3. **SAVE TRANSACTION**: Tạo savepoint để rollback từng phần
4. **Monitoring**: Xem log và trạng thái transaction qua DMV
5. **Tính nguyên tử**: Đảm bảo tất cả thao tác thành công hoặc tất cả thất bại

**Tính năng mới SQL Server 2022:**
- **ADR**: Recovery nhanh hơn
- **Ledger Tables**: Bảo vệ tính toàn vẹn dữ liệu
- **Intelligent Query Processing**: Tối ưu hóa tự động
- **JSON Support**: Xử lý JSON hiệu quả hơn
- **Time Series Functions**: Phân tích theo thời gian
- **Improved Deadlock Detection**: Phát hiện deadlock tốt hơn

SQL Server 2022 làm cho transaction **nhanh hơn**, **an toàn hơn** và **dễ quản lý hơn** so với các phiên bản trước.