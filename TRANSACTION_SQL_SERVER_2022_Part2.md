# TRANSACTION TRONG SQL SERVER 2022 - PHẦN 2

### 3.4. Thực Hiện Transaction Chuyển Tiền

```sql
-- Stored Procedure để chuyển tiền với Transaction
CREATE PROCEDURE sp_TransferMoney
    @FromAccountID INT,
    @ToAccountID INT,
    @Amount DECIMAL(18,2),
    @Description NVARCHAR(500)
AS
BEGIN
    SET NOCOUNT ON;
    
    DECLARE @FromBalance DECIMAL(18,2);
    DECLARE @ToBalance DECIMAL(18,2);
    DECLARE @ReferenceNumber NVARCHAR(50);
    DECLARE @ErrorMessage NVARCHAR(500);
    
    -- Tạo reference number
    SET @ReferenceNumber = 'TXN' + FORMAT(GETDATE(), 'yyyyMMddHHmmss') + 
                          RIGHT('000' + CAST(@FromAccountID AS NVARCHAR), 3);
    
    BEGIN TRY
        BEGIN TRANSACTION TransferMoney;
        
        -- Bước 1: Kiểm tra tài khoản nguồn tồn tại và đang hoạt động
        IF NOT EXISTS (SELECT 1 FROM Accounts WHERE AccountID = @FromAccountID AND Status = 'ACTIVE')
        BEGIN
            SET @ErrorMessage = N'Tài khoản nguồn không tồn tại hoặc không hoạt động';
            THROW 50001, @ErrorMessage, 1;
        END
        
        -- Bước 2: Kiểm tra tài khoản đích tồn tại và đang hoạt động
        IF NOT EXISTS (SELECT 1 FROM Accounts WHERE AccountID = @ToAccountID AND Status = 'ACTIVE')
        BEGIN
            SET @ErrorMessage = N'Tài khoản đích không tồn tại hoặc không hoạt động';
            THROW 50002, @ErrorMessage, 1;
        END
        
        -- Bước 3: Kiểm tra số tiền hợp lệ
        IF @Amount <= 0
        BEGIN
            SET @ErrorMessage = N'Số tiền chuyển phải lớn hơn 0';
            THROW 50003, @ErrorMessage, 1;
        END
        
        -- Bước 4: Lấy số dư hiện tại của tài khoản nguồn
        SELECT @FromBalance = Balance 
        FROM Accounts WITH (UPDLOCK, HOLDLOCK)
        WHERE AccountID = @FromAccountID;
        
        -- Bước 5: Kiểm tra số dư đủ để chuyển
        IF @FromBalance < @Amount
        BEGIN
            SET @ErrorMessage = N'Số dư không đủ để thực hiện giao dịch. Số dư hiện tại: ' + 
                              CAST(@FromBalance AS NVARCHAR(50));
            THROW 50004, @ErrorMessage, 1;
        END
        
        -- Tạo savepoint sau khi validate
        SAVE TRANSACTION ValidationComplete;
        
        -- Bước 6: Ghi log audit trước khi thay đổi
        INSERT INTO AuditLog (TableName, Operation, OldValue, NewValue)
        VALUES (
            'Accounts',
            'TRANSFER_DEBIT',
            'AccountID: ' + CAST(@FromAccountID AS NVARCHAR) + ', Balance: ' + CAST(@FromBalance AS NVARCHAR),
            'AccountID: ' + CAST(@FromAccountID AS NVARCHAR) + ', Balance: ' + CAST(@FromBalance - @Amount AS NVARCHAR)
        );
        
        -- Bước 7: Trừ tiền từ tài khoản nguồn
        UPDATE Accounts
        SET Balance = Balance - @Amount,
            LastModified = GETDATE()
        WHERE AccountID = @FromAccountID;
        
        -- Kiểm tra update thành công
        IF @@ROWCOUNT = 0
        BEGIN
            ROLLBACK TRANSACTION TransferMoney;
            SET @ErrorMessage = N'Không thể cập nhật tài khoản nguồn';
            THROW 50005, @ErrorMessage, 1;
        END
        
        -- Tạo savepoint sau khi trừ tiền
        SAVE TRANSACTION DebitComplete;
        
        -- Bước 8: Lấy số dư hiện tại của tài khoản đích
        SELECT @ToBalance = Balance 
        FROM Accounts WITH (UPDLOCK, HOLDLOCK)
        WHERE AccountID = @ToAccountID;
        
        -- Bước 9: Ghi log audit cho tài khoản đích
        INSERT INTO AuditLog (TableName, Operation, OldValue, NewValue)
        VALUES (
            'Accounts',
            'TRANSFER_CREDIT',
            'AccountID: ' + CAST(@ToAccountID AS NVARCHAR) + ', Balance: ' + CAST(@ToBalance AS NVARCHAR),
            'AccountID: ' + CAST(@ToAccountID AS NVARCHAR) + ', Balance: ' + CAST(@ToBalance + @Amount AS NVARCHAR)
        );
        
        -- Bước 10: Cộng tiền vào tài khoản đích
        UPDATE Accounts
        SET Balance = Balance + @Amount,
            LastModified = GETDATE()
        WHERE AccountID = @ToAccountID;
        
        -- Kiểm tra update thành công
        IF @@ROWCOUNT = 0
        BEGIN
            ROLLBACK TRANSACTION TransferMoney;
            SET @ErrorMessage = N'Không thể cập nhật tài khoản đích';
            THROW 50006, @ErrorMessage, 1;
        END
        
        -- Tạo savepoint sau khi cộng tiền
        SAVE TRANSACTION CreditComplete;
        
        -- Bước 11: Ghi lịch sử giao dịch
        INSERT INTO TransactionHistory (
            FromAccountID, 
            ToAccountID, 
            Amount, 
            TransactionType, 
            Status, 
            Description, 
            ReferenceNumber
        )
        VALUES (
            @FromAccountID,
            @ToAccountID,
            @Amount,
            'TRANSFER',
            'COMPLETED',
            @Description,
            @ReferenceNumber
        );
        
        -- Bước 12: Commit transaction nếu tất cả thành công
        COMMIT TRANSACTION TransferMoney;
        
        -- Thông báo thành công
        PRINT N'Giao dịch thành công!';
        PRINT N'Mã giao dịch: ' + @ReferenceNumber;
        PRINT N'Số tiền: ' + CAST(@Amount AS NVARCHAR(50)) + ' VND';
        PRINT N'Từ tài khoản: ' + CAST(@FromAccountID AS NVARCHAR);
        PRINT N'Đến tài khoản: ' + CAST(@ToAccountID AS NVARCHAR);
        
    END TRY
    BEGIN CATCH
        -- Rollback nếu có lỗi
        IF @@TRANCOUNT > 0
        BEGIN
            ROLLBACK TRANSACTION TransferMoney;
        END
        
        -- Ghi log lỗi
        INSERT INTO AuditLog (TableName, Operation, OldValue, NewValue)
        VALUES (
            'TransactionHistory',
            'TRANSFER_FAILED',
            'Error: ' + ERROR_MESSAGE(),
            'FromAccount: ' + CAST(@FromAccountID AS NVARCHAR) + 
            ', ToAccount: ' + CAST(@ToAccountID AS NVARCHAR) + 
            ', Amount: ' + CAST(@Amount AS NVARCHAR)
        );
        
        -- Hiển thị thông báo lỗi
        PRINT N'Giao dịch thất bại!';
        PRINT N'Lỗi: ' + ERROR_MESSAGE();
        PRINT N'Mã lỗi: ' + CAST(ERROR_NUMBER() AS NVARCHAR);
        PRINT N'Dòng lỗi: ' + CAST(ERROR_LINE() AS NVARCHAR);
        
        -- Throw lại lỗi
        THROW;
    END CATCH
END;
GO
```

### 3.5. Thực Hiện Giao Dịch Thành Công

```sql
-- Chuyển 2,000,000 VND từ tài khoản 1 sang tài khoản 2
EXEC sp_TransferMoney 
    @FromAccountID = 1,
    @ToAccountID = 2,
    @Amount = 2000000.00,
    @Description = N'Chuyển tiền thanh toán hóa đơn';

/*
Kết quả:
Giao dịch thành công!
Mã giao dịch: TXN20241215143025001
Số tiền: 2000000.00 VND
Từ tài khoản: 1
Đến tài khoản: 2
*/
```

### 3.6. Demo Kết Quả SAU khi Transaction

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
Kết quả:
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
    TransactionType,
    TransactionDate,
    Status,
    Description,
    ReferenceNumber
FROM TransactionHistory
ORDER BY TransactionDate DESC;

/*
Kết quả:
TransactionID | FromAccountID | ToAccountID | Amount      | TransactionType | TransactionDate      | Status    | Description                      | ReferenceNumber
--------------|---------------|-------------|-------------|-----------------|----------------------|-----------|----------------------------------|------------------
1             | 1             | 2           | 2000000.00  | TRANSFER        | 2024-12-15 14:30:25  | COMPLETED | Chuyển tiền thanh toán hóa đơn   | TXN20241215143025001
*/

-- Xem audit log
SELECT 
    AuditID,
    TableName,
    Operation,
    OldValue,
    NewValue,
    ModifiedBy,
    ModifiedDate
FROM AuditLog
ORDER BY ModifiedDate DESC;

/*
Kết quả:
AuditID | TableName | Operation        | OldValue                              | NewValue                              | ModifiedBy | ModifiedDate
--------|-----------|------------------|---------------------------------------|---------------------------------------|------------|------------------
3       | Accounts  | TRANSFER_CREDIT  | AccountID: 2, Balance: 5000000.00     | AccountID: 2, Balance: 7000000.00     | sa         | 2024-12-15 14:30:25
2       | Accounts  | TRANSFER_DEBIT   | AccountID: 1, Balance: 10000000.00    | AccountID: 1, Balance: 8000000.00     | sa         | 2024-12-15 14:30:25
1       | Accounts  | TRANSFER_DEBIT   | AccountID: 1, Balance: 10000000.00    | AccountID: 1, Balance: 8000000.00     | sa         | 2024-12-15 14:30:25
*/
```

### 3.7. Demo Giao Dịch Thất Bại (Số Dư Không Đủ)

```sql
-- Thử chuyển 15,000,000 VND từ tài khoản 1 (chỉ còn 8,000,000)
EXEC sp_TransferMoney 
    @FromAccountID = 1,
    @ToAccountID = 2,
    @Amount = 15000000.00,
    @Description = N'Chuyển tiền mua nhà';

/*
Kết quả:
Giao dịch thất bại!
Lỗi: Số dư không đủ để thực hiện giao dịch. Số dư hiện tại: 8000000.00
Mã lỗi: 50004
Dòng lỗi: 45
*/

-- Kiểm tra số dư không thay đổi
SELECT AccountID, Balance FROM Accounts WHERE AccountID = 1;
/*
Kết quả:
AccountID | Balance
----------|------------
1         | 8000000.00

Giải thích: Transaction đã ROLLBACK, số dư không thay đổi
*/

-- Kiểm tra audit log ghi nhận lỗi
SELECT TOP 1
    Operation,
    OldValue,
    NewValue,
    ModifiedDate
FROM AuditLog
WHERE Operation = 'TRANSFER_FAILED'
ORDER BY ModifiedDate DESC;

/*
Kết quả:
Operation        | OldValue                                                          | NewValue                                      | ModifiedDate
-----------------|-------------------------------------------------------------------|-----------------------------------------------|------------------
TRANSFER_FAILED  | Error: Số dư không đủ để thực hiện giao dịch. Số dư hiện tại: 8000000.00 | FromAccount: 1, ToAccount: 2, Amount: 15000000.00 | 2024-12-15 14:35:10
*/
```
