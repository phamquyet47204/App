# TRANSACTION TRONG SQL SERVER 2022 - PHẦN 4

## 4. TÍNH NĂNG MỚI VÀ CẢI TIẾN TRONG SQL SERVER 2022

### 4.1. Accelerated Database Recovery (ADR) - Cải Tiến

SQL Server 2022 cải tiến tính năng Accelerated Database Recovery (ADR) giúp quá trình recovery nhanh hơn và ổn định hơn.

```sql
-- Bật ADR cho database
ALTER DATABASE BankingSystem SET ACCELERATED_DATABASE_RECOVERY = ON;

-- Kiểm tra trạng thái ADR
SELECT 
    name AS DatabaseName,
    is_accelerated_database_recovery_on AS ADR_Enabled
FROM sys.databases
WHERE name = 'BankingSystem';

/*
Lợi ích của ADR:
1. Recovery nhanh hơn sau khi crash
2. Rollback transaction dài nhanh hơn
3. Truncate log hiệu quả hơn
4. Giảm thời gian downtime
*/

-- Demo: Transaction dài với ADR
BEGIN TRANSACTION LongTransaction;

-- Thực hiện nhiều thao tác
DECLARE @i INT = 1;
WHILE @i <= 10000
BEGIN
    INSERT INTO TransactionHistory (FromAccountID, ToAccountID, Amount, TransactionType, Status, ReferenceNumber)
    VALUES (1, 2, 1000, 'TEST', 'COMPLETED', 'TEST' + CAST(@i AS NVARCHAR));
    SET @i = @i + 1;
END

-- Rollback sẽ nhanh hơn với ADR
ROLLBACK TRANSACTION LongTransaction;

PRINT N'Rollback hoàn tất nhanh chóng nhờ ADR';
```

### 4.2. Transaction Snapshot Isolation Improvements

SQL Server 2022 cải thiện hiệu suất của Snapshot Isolation Level.

```sql
-- Bật Snapshot Isolation
ALTER DATABASE BankingSystem SET ALLOW_SNAPSHOT_ISOLATION ON;
ALTER DATABASE BankingSystem SET READ_COMMITTED_SNAPSHOT ON;

-- Demo: Đọc dữ liệu không bị block bởi transaction khác
-- Session 1: Bắt đầu transaction và giữ lock
BEGIN TRANSACTION;
UPDATE Accounts SET Balance = Balance - 100000 WHERE AccountID = 1;
WAITFOR DELAY '00:00:10'; -- Giữ lock 10 giây

-- Session 2: Đọc dữ liệu với Snapshot Isolation (không bị block)
SET TRANSACTION ISOLATION LEVEL SNAPSHOT;
BEGIN TRANSACTION;

SELECT AccountID, Balance 
FROM Accounts 
WHERE AccountID = 1;
-- Trả về giá trị trước khi Session 1 update (không bị block)

COMMIT TRANSACTION;

-- Session 1: Commit
COMMIT TRANSACTION;
```

### 4.3. Intelligent Query Processing Enhancements

SQL Server 2022 cải thiện xử lý query trong transaction với Memory Grant Feedback và Cardinality Estimation.

```sql
-- Bật Intelligent Query Processing
ALTER DATABASE BankingSystem SET COMPATIBILITY_LEVEL = 160; -- SQL Server 2022

-- Demo: Query với Memory Grant Feedback
BEGIN TRANSACTION;

-- Query phức tạp với nhiều join
SELECT 
    C.CustomerName,
    A.AccountNumber,
    COUNT(TH.TransactionID) AS TotalTransactions,
    SUM(TH.Amount) AS TotalAmount,
    AVG(TH.Amount) AS AvgAmount
FROM Customers C
INNER JOIN Accounts A ON C.CustomerID = A.CustomerID
LEFT JOIN TransactionHistory TH ON A.AccountID = TH.FromAccountID
WHERE TH.TransactionDate >= DATEADD(MONTH, -6, GETDATE())
GROUP BY C.CustomerName, A.AccountNumber
HAVING COUNT(TH.TransactionID) > 5
ORDER BY TotalAmount DESC;

COMMIT TRANSACTION;

-- SQL Server 2022 tự động điều chỉnh memory grant cho lần chạy tiếp theo
```

### 4.4. Ledger Tables - Tính Năng Mới

SQL Server 2022 giới thiệu Ledger Tables để đảm bảo tính toàn vẹn dữ liệu không thể thay đổi.

Cấu trúc table:
```
LedgerAccounts (AccountID, Balance, LastModified)
LedgerTransactionHistory (TransactionID, FromAccountID, ToAccountID, Amount, TransactionDate)
```

```sql
-- Tạo Ledger Table cho Accounts
CREATE TABLE LedgerAccounts (
    AccountID INT NOT NULL,
    AccountNumber NVARCHAR(20) NOT NULL,
    Balance DECIMAL(18,2) NOT NULL,
    LastModified DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME()
)
WITH (
    SYSTEM_VERSIONING = ON,
    LEDGER = ON (
        LEDGER_VIEW = LedgerAccountsView (
            TRANSACTION_ID_COLUMN_NAME = ledger_transaction_id,
            SEQUENCE_NUMBER_COLUMN_NAME = ledger_sequence_number,
            OPERATION_TYPE_COLUMN_NAME = ledger_operation_type,
            OPERATION_TYPE_DESC_COLUMN_NAME = ledger_operation_type_desc
        )
    )
);

-- Tạo Ledger Table cho Transaction History
CREATE TABLE LedgerTransactionHistory (
    TransactionID INT IDENTITY(1,1) NOT NULL,
    FromAccountID INT NOT NULL,
    ToAccountID INT NOT NULL,
    Amount DECIMAL(18,2) NOT NULL,
    TransactionDate DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(),
    Status NVARCHAR(20) NOT NULL
)
WITH (
    LEDGER = ON
);

-- Insert dữ liệu vào Ledger Table
BEGIN TRANSACTION;

INSERT INTO LedgerAccounts (AccountID, AccountNumber, Balance)
VALUES (1, 'LED001', 10000000.00);

INSERT INTO LedgerAccounts (AccountID, AccountNumber, Balance)
VALUES (2, 'LED002', 5000000.00);

COMMIT TRANSACTION;

-- Thực hiện chuyển tiền với Ledger
BEGIN TRANSACTION LedgerTransfer;

-- Trừ tiền tài khoản 1
UPDATE LedgerAccounts 
SET Balance = Balance - 1000000.00,
    LastModified = SYSUTCDATETIME()
WHERE AccountID = 1;

-- Cộng tiền tài khoản 2
UPDATE LedgerAccounts 
SET Balance = Balance + 1000000.00,
    LastModified = SYSUTCDATETIME()
WHERE AccountID = 2;

-- Ghi lịch sử
INSERT INTO LedgerTransactionHistory (FromAccountID, ToAccountID, Amount, Status)
VALUES (1, 2, 1000000.00, 'COMPLETED');

COMMIT TRANSACTION LedgerTransfer;

-- Xem ledger history (không thể xóa hoặc sửa)
SELECT 
    AccountID,
    Balance,
    LastModified,
    ledger_transaction_id,
    ledger_sequence_number,
    ledger_operation_type_desc
FROM LedgerAccountsView
ORDER BY ledger_sequence_number;

/*
Kết quả:
AccountID | Balance      | LastModified            | ledger_transaction_id | ledger_sequence_number | ledger_operation_type_desc
----------|--------------|-------------------------|----------------------|------------------------|---------------------------
1         | 10000000.00  | 2024-12-15 14:00:00     | 1                    | 0                      | INSERT
2         | 5000000.00   | 2024-12-15 14:00:00     | 1                    | 1                      | INSERT
1         | 9000000.00   | 2024-12-15 14:05:00     | 2                    | 2                      | UPDATE
2         | 6000000.00   | 2024-12-15 14:05:00     | 2                    | 3                      | UPDATE

Giải thích: Mọi thay đổi đều được ghi lại và không thể xóa
*/

-- Verify ledger integrity
EXEC sp_verify_database_ledger;

/*
Kết quả:
verified: 1
Giải thích: Dữ liệu ledger không bị can thiệp
*/
```

### 4.5. Contained Availability Groups

SQL Server 2022 hỗ trợ Contained Availability Groups cho transaction replication tốt hơn.

```sql
-- Tạo Contained Availability Group
CREATE AVAILABILITY GROUP ContainedAG
WITH (
    AUTOMATED_BACKUP_PREFERENCE = SECONDARY,
    DB_FAILOVER = ON,
    CONTAINED
)
FOR DATABASE BankingSystem
REPLICA ON 
    'Server1' WITH (
        ENDPOINT_URL = 'TCP://Server1:5022',
        AVAILABILITY_MODE = SYNCHRONOUS_COMMIT,
        FAILOVER_MODE = AUTOMATIC,
        SEEDING_MODE = AUTOMATIC
    ),
    'Server2' WITH (
        ENDPOINT_URL = 'TCP://Server2:5022',
        AVAILABILITY_MODE = SYNCHRONOUS_COMMIT,
        FAILOVER_MODE = AUTOMATIC,
        SEEDING_MODE = AUTOMATIC
    );

-- Transaction sẽ được replicate tự động sang secondary replica
BEGIN TRANSACTION;

UPDATE Accounts SET Balance = Balance + 1000000 WHERE AccountID = 1;

COMMIT TRANSACTION;
-- Transaction được commit trên cả primary và secondary replica
```

### 4.6. Parameter Sensitive Plan Optimization

SQL Server 2022 tự động tạo nhiều execution plan cho các parameter khác nhau.

```sql
-- Tạo stored procedure với parameter sensitive plan
CREATE PROCEDURE sp_GetTransactionHistory
    @AccountID INT,
    @StartDate DATE,
    @EndDate DATE
AS
BEGIN
    SELECT 
        TransactionID,
        FromAccountID,
        ToAccountID,
        Amount,
        TransactionDate,
        Status
    FROM TransactionHistory
    WHERE (FromAccountID = @AccountID OR ToAccountID = @AccountID)
        AND TransactionDate BETWEEN @StartDate AND @EndDate
    ORDER BY TransactionDate DESC
    OPTION (USE HINT('PARAMETER_SENSITIVE_PLAN_OPTIMIZATION'));
END;
GO

-- SQL Server 2022 sẽ tạo plan khác nhau cho:
-- 1. Query với ít records (vài ngày)
EXEC sp_GetTransactionHistory 
    @AccountID = 1,
    @StartDate = '2024-12-01',
    @EndDate = '2024-12-05';

-- 2. Query với nhiều records (cả năm)
EXEC sp_GetTransactionHistory 
    @AccountID = 1,
    @StartDate = '2024-01-01',
    @EndDate = '2024-12-31';

-- Mỗi trường hợp sẽ có execution plan tối ưu riêng
```

### 4.7. Tempdb Metadata Memory-Optimized

SQL Server 2022 cải thiện hiệu suất tempdb cho transaction với nhiều temp table.

```sql
-- Bật memory-optimized tempdb metadata
ALTER SERVER CONFIGURATION SET MEMORY_OPTIMIZED TEMPDB_METADATA = ON;
-- Yêu cầu restart SQL Server

-- Demo: Transaction với nhiều temp table
BEGIN TRANSACTION;

-- Tạo temp table để xử lý
CREATE TABLE #TempTransactions (
    TransactionID INT,
    Amount DECIMAL(18,2),
    ProcessedDate DATETIME
);

-- Insert nhiều records
INSERT INTO #TempTransactions
SELECT 
    TransactionID,
    Amount,
    GETDATE()
FROM TransactionHistory
WHERE TransactionDate >= DATEADD(DAY, -30, GETDATE());

-- Xử lý dữ liệu
UPDATE A
SET A.Balance = A.Balance + T.TotalAmount
FROM Accounts A
INNER JOIN (
    SELECT 
        ToAccountID,
        SUM(Amount) AS TotalAmount
    FROM #TempTransactions
    GROUP BY ToAccountID
) T ON A.AccountID = T.ToAccountID;

DROP TABLE #TempTransactions;

COMMIT TRANSACTION;

-- Với memory-optimized tempdb, transaction này chạy nhanh hơn
```


### 4.8. Resumable Operations for Transactions

SQL Server 2022 hỗ trợ resumable operations cho các thao tác lớn trong transaction.

```sql
-- Tạo index với resumable option
CREATE INDEX IX_TransactionHistory_Date 
ON TransactionHistory(TransactionDate)
WITH (RESUMABLE = ON, MAX_DURATION = 60);

-- Nếu operation bị gián đoạn, có thể resume
ALTER INDEX IX_TransactionHistory_Date 
ON TransactionHistory 
RESUME;

-- Kiểm tra trạng thái resumable operations
SELECT 
    name,
    sql_text,
    state_desc,
    percent_complete,
    start_time,
    last_pause_time
FROM sys.index_resumable_operations;
```

### 4.9. Improved Transaction Log Management

SQL Server 2022 cải thiện quản lý transaction log với auto-growth tốt hơn.

```sql
-- Cấu hình transaction log với auto-growth thông minh
ALTER DATABASE BankingSystem
MODIFY FILE (
    NAME = BankingSystem_log,
    SIZE = 1GB,
    FILEGROWTH = 512MB,
    MAXSIZE = 50GB
);

-- Xem thông tin log file
SELECT 
    name AS LogName,
    physical_name AS PhysicalPath,
    size * 8 / 1024 AS CurrentSizeMB,
    max_size * 8 / 1024 AS MaxSizeMB,
    growth * 8 / 1024 AS GrowthMB,
    is_percent_growth
FROM sys.database_files
WHERE type_desc = 'LOG';

-- Monitor log space usage
SELECT 
    DB_NAME(database_id) AS DatabaseName,
    total_log_size_in_bytes / 1024 / 1024 AS TotalLogSizeMB,
    used_log_space_in_bytes / 1024 / 1024 AS UsedLogSpaceMB,
    used_log_space_in_percent AS UsedLogSpacePercent,
    log_space_in_bytes_since_last_backup / 1024 / 1024 AS LogSpaceSinceBackupMB
FROM sys.dm_db_log_space_usage
WHERE database_id = DB_ID('BankingSystem');
```

### 4.10. Enhanced Distributed Transactions

SQL Server 2022 cải thiện distributed transaction với Azure SQL Database.

```sql
-- Tạo linked server
EXEC sp_addlinkedserver 
    @server = 'RemoteServer',
    @srvproduct = '',
    @provider = 'SQLNCLI',
    @datasrc = 'remote.database.windows.net';

-- Distributed transaction giữa 2 server
BEGIN DISTRIBUTED TRANSACTION;

-- Update trên local server
UPDATE BankingSystem.dbo.Accounts 
SET Balance = Balance - 1000000 
WHERE AccountID = 1;

-- Update trên remote server
UPDATE RemoteServer.RemoteDB.dbo.Accounts 
SET Balance = Balance + 1000000 
WHERE AccountID = 2;

-- Commit trên cả 2 server
COMMIT TRANSACTION;

/*
SQL Server 2022 cải thiện:
1. Hiệu suất distributed transaction
2. Độ tin cậy khi network không ổn định
3. Tích hợp tốt hơn với Azure
*/
```

### 4.11. JSON Support in Transactions

SQL Server 2022 cải thiện xử lý JSON trong transaction.

Cấu trúc table:
```
TransactionMetadata (
    TransactionID INT PRIMARY KEY,
    MetadataJSON NVARCHAR(MAX),
    CreatedDate DATETIME
)
```

```sql
-- Tạo table với JSON column
CREATE TABLE TransactionMetadata (
    TransactionID INT PRIMARY KEY IDENTITY,
    MetadataJSON NVARCHAR(MAX),
    CreatedDate DATETIME DEFAULT GETDATE(),
    CONSTRAINT CK_MetadataJSON CHECK (ISJSON(MetadataJSON) = 1)
);

-- Transaction với JSON data
BEGIN TRANSACTION;

DECLARE @TransactionData NVARCHAR(MAX) = N'{
    "transactionType": "TRANSFER",
    "fromAccount": {
        "accountId": 1,
        "accountNumber": "ACC001",
        "previousBalance": 10000000.00
    },
    "toAccount": {
        "accountId": 2,
        "accountNumber": "ACC002",
        "previousBalance": 5000000.00
    },
    "amount": 2000000.00,
    "fee": 5000.00,
    "timestamp": "2024-12-15T14:30:25",
    "ipAddress": "192.168.1.100",
    "deviceInfo": {
        "type": "mobile",
        "os": "iOS",
        "appVersion": "2.1.0"
    }
}';

-- Insert JSON data
INSERT INTO TransactionMetadata (MetadataJSON)
VALUES (@TransactionData);

-- Query JSON data trong transaction
SELECT 
    TransactionID,
    JSON_VALUE(MetadataJSON, '$.transactionType') AS TransactionType,
    JSON_VALUE(MetadataJSON, '$.amount') AS Amount,
    JSON_VALUE(MetadataJSON, '$.fromAccount.accountNumber') AS FromAccount,
    JSON_VALUE(MetadataJSON, '$.toAccount.accountNumber') AS ToAccount,
    JSON_VALUE(MetadataJSON, '$.deviceInfo.type') AS DeviceType
FROM TransactionMetadata;

COMMIT TRANSACTION;
```

### 4.12. Improved Deadlock Detection

SQL Server 2022 cải thiện phát hiện và xử lý deadlock.

```sql
-- Bật extended events để monitor deadlock
CREATE EVENT SESSION DeadlockMonitor ON SERVER
ADD EVENT sqlserver.database_xml_deadlock_report
ADD TARGET package0.event_file(SET filename=N'C:\Logs\Deadlocks.xel')
WITH (MAX_MEMORY=4096 KB, EVENT_RETENTION_MODE=ALLOW_SINGLE_EVENT_LOSS);

ALTER EVENT SESSION DeadlockMonitor ON SERVER STATE = START;

-- Demo: Tạo deadlock scenario
-- Session 1:
BEGIN TRANSACTION;
UPDATE Accounts SET Balance = Balance + 1000 WHERE AccountID = 1;
WAITFOR DELAY '00:00:05';
UPDATE Accounts SET Balance = Balance + 1000 WHERE AccountID = 2;
COMMIT TRANSACTION;

-- Session 2 (chạy đồng thời):
BEGIN TRANSACTION;
UPDATE Accounts SET Balance = Balance + 1000 WHERE AccountID = 2;
WAITFOR DELAY '00:00:05';
UPDATE Accounts SET Balance = Balance + 1000 WHERE AccountID = 1;
COMMIT TRANSACTION;

-- SQL Server 2022 phát hiện deadlock nhanh hơn và chọn victim tối ưu hơn

-- Xem deadlock graph
SELECT 
    CAST(event_data AS XML) AS DeadlockGraph
FROM sys.fn_xe_file_target_read_file('C:\Logs\Deadlocks*.xel', NULL, NULL, NULL);
```

### 4.13. Batch Mode on Rowstore

SQL Server 2022 mở rộng batch mode processing cho rowstore tables trong transaction.

```sql
-- Bật batch mode
ALTER DATABASE BankingSystem SET COMPATIBILITY_LEVEL = 160;

-- Query sử dụng batch mode
BEGIN TRANSACTION;

SELECT 
    YEAR(TransactionDate) AS Year,
    MONTH(TransactionDate) AS Month,
    COUNT(*) AS TotalTransactions,
    SUM(Amount) AS TotalAmount,
    AVG(Amount) AS AvgAmount,
    MIN(Amount) AS MinAmount,
    MAX(Amount) AS MaxAmount
FROM TransactionHistory
WHERE TransactionDate >= '2023-01-01'
GROUP BY YEAR(TransactionDate), MONTH(TransactionDate)
ORDER BY Year, Month
OPTION (USE HINT('DISALLOW_BATCH_MODE')); -- So sánh với row mode

-- Chạy lại với batch mode (mặc định)
SELECT 
    YEAR(TransactionDate) AS Year,
    MONTH(TransactionDate) AS Month,
    COUNT(*) AS TotalTransactions,
    SUM(Amount) AS TotalAmount,
    AVG(Amount) AS AvgAmount,
    MIN(Amount) AS MinAmount,
    MAX(Amount) AS MaxAmount
FROM TransactionHistory
WHERE TransactionDate >= '2023-01-01'
GROUP BY YEAR(TransactionDate), MONTH(TransactionDate)
ORDER BY Year, Month;
-- Batch mode nhanh hơn đáng kể

COMMIT TRANSACTION;
```

### 4.14. Approximate Percentile Functions

SQL Server 2022 thêm approximate percentile functions cho transaction analytics.

```sql
-- Sử dụng APPROX_PERCENTILE_CONT và APPROX_PERCENTILE_DISC
BEGIN TRANSACTION;

SELECT 
    APPROX_PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY Amount) AS MedianAmount,
    APPROX_PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY Amount) AS Q1Amount,
    APPROX_PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY Amount) AS Q3Amount,
    APPROX_PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY Amount) AS P95Amount,
    APPROX_PERCENTILE_CONT(0.99) WITHIN GROUP (ORDER BY Amount) AS P99Amount
FROM TransactionHistory
WHERE TransactionDate >= DATEADD(MONTH, -1, GETDATE());

/*
Kết quả:
MedianAmount | Q1Amount   | Q3Amount   | P95Amount   | P99Amount
-------------|------------|------------|-------------|------------
500000.00    | 200000.00  | 1000000.00 | 5000000.00  | 10000000.00

Giải thích: Nhanh hơn PERCENTILE_CONT chính xác
*/

COMMIT TRANSACTION;
```

### 4.15. Time Series Functions

SQL Server 2022 thêm các hàm time series hữu ích cho transaction analysis.

```sql
-- Sử dụng DATE_BUCKET và GENERATE_SERIES
BEGIN TRANSACTION;

-- Phân tích transaction theo bucket thời gian
SELECT 
    DATE_BUCKET(HOUR, 1, TransactionDate) AS TimeWindow,
    COUNT(*) AS TransactionCount,
    SUM(Amount) AS TotalAmount,
    AVG(Amount) AS AvgAmount
FROM TransactionHistory
WHERE TransactionDate >= DATEADD(DAY, -7, GETDATE())
GROUP BY DATE_BUCKET(HOUR, 1, TransactionDate)
ORDER BY TimeWindow;

/*
Kết quả:
TimeWindow           | TransactionCount | TotalAmount  | AvgAmount
---------------------|------------------|--------------|------------
2024-12-15 08:00:00  | 45               | 25000000.00  | 555555.56
2024-12-15 09:00:00  | 67               | 38000000.00  | 567164.18
2024-12-15 10:00:00  | 89               | 52000000.00  | 584269.66
*/

-- Tạo time series với GENERATE_SERIES
SELECT 
    value AS HourOfDay,
    ISNULL(T.TransactionCount, 0) AS TransactionCount,
    ISNULL(T.TotalAmount, 0) AS TotalAmount
FROM GENERATE_SERIES(0, 23, 1) AS Hours
LEFT JOIN (
    SELECT 
        DATEPART(HOUR, TransactionDate) AS Hour,
        COUNT(*) AS TransactionCount,
        SUM(Amount) AS TotalAmount
    FROM TransactionHistory
    WHERE CAST(TransactionDate AS DATE) = CAST(GETDATE() AS DATE)
    GROUP BY DATEPART(HOUR, TransactionDate)
) T ON Hours.value = T.Hour
ORDER BY Hours.value;

COMMIT TRANSACTION;
```

## KẾT LUẬN

SQL Server 2022 mang đến nhiều cải tiến quan trọng cho xử lý transaction:

1. **Accelerated Database Recovery (ADR)**: Recovery và rollback nhanh hơn
2. **Ledger Tables**: Đảm bảo tính toàn vẹn dữ liệu không thể thay đổi
3. **Intelligent Query Processing**: Tối ưu hóa query tự động
4. **Parameter Sensitive Plan**: Execution plan linh hoạt theo parameter
5. **Improved Deadlock Detection**: Phát hiện và xử lý deadlock tốt hơn
6. **Batch Mode on Rowstore**: Hiệu suất xử lý cao hơn
7. **Time Series Functions**: Phân tích transaction theo thời gian dễ dàng
8. **JSON Support**: Xử lý dữ liệu JSON hiệu quả trong transaction
9. **Resumable Operations**: Tiếp tục operations bị gián đoạn
10. **Enhanced Distributed Transactions**: Tích hợp tốt hơn với Azure

Các tính năng này giúp transaction trong SQL Server 2022 nhanh hơn, an toàn hơn và dễ quản lý hơn so với các phiên bản trước.
