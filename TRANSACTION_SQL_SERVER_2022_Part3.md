# TRANSACTION TRONG SQL SERVER 2022 - PHẦN 3

### 3.8. Demo Sử Dụng ROLLBACK với Điều Kiện

```sql
-- Tạo stored procedure với điều kiện rollback
CREATE PROCEDURE sp_TransferWithLimit
    @FromAccountID INT,
    @ToAccountID INT,
    @Amount DECIMAL(18,2),
    @DailyLimit DECIMAL(18,2) = 10000000.00
AS
BEGIN
    DECLARE @TodayTotal DECIMAL(18,2);
    
    BEGIN TRANSACTION;
    
    -- Tính tổng số tiền đã chuyển trong ngày
    SELECT @TodayTotal = ISNULL(SUM(Amount), 0)
    FROM TransactionHistory
    WHERE FromAccountID = @FromAccountID
        AND CAST(TransactionDate AS DATE) = CAST(GETDATE() AS DATE)
        AND Status = 'COMPLETED';
    
    -- Kiểm tra vượt hạn mức
    IF (@TodayTotal + @Amount) > @DailyLimit
    BEGIN
        ROLLBACK TRANSACTION;
        PRINT N'Giao dịch bị từ chối: Vượt hạn mức chuyển tiền trong ngày';
        PRINT N'Hạn mức: ' + CAST(@DailyLimit AS NVARCHAR(50));
        PRINT N'Đã chuyển: ' + CAST(@TodayTotal AS NVARCHAR(50));
        PRINT N'Số tiền yêu cầu: ' + CAST(@Amount AS NVARCHAR(50));
        RETURN;
    END
    
    -- Thực hiện chuyển tiền
    UPDATE Accounts SET Balance = Balance - @Amount WHERE AccountID = @FromAccountID;
    UPDATE Accounts SET Balance = Balance + @Amount WHERE AccountID = @ToAccountID;
    
    INSERT INTO TransactionHistory (FromAccountID, ToAccountID, Amount, TransactionType, Status, ReferenceNumber)
    VALUES (@FromAccountID, @ToAccountID, @Amount, 'TRANSFER', 'COMPLETED', 
            'TXN' + FORMAT(GETDATE(), 'yyyyMMddHHmmss'));
    
    COMMIT TRANSACTION;
    PRINT N'Giao dịch thành công!';
END;
GO

-- Test với giao dịch vượt hạn mức
EXEC sp_TransferWithLimit 
    @FromAccountID = 1,
    @ToAccountID = 2,
    @Amount = 9000000.00,
    @DailyLimit = 10000000.00;

/*
Kết quả:
Giao dịch bị từ chối: Vượt hạn mức chuyển tiền trong ngày
Hạn mức: 10000000.00
Đã chuyển: 2000000.00
Số tiền yêu cầu: 9000000.00

Giải thích: 2,000,000 (đã chuyển) + 9,000,000 (yêu cầu) = 11,000,000 > 10,000,000 (hạn mức)
*/
```

### 3.9. Demo Transaction với Multiple Savepoints

Cấu trúc table:
```
Accounts (AccountID, Balance, Status)
TransactionHistory (TransactionID, FromAccountID, ToAccountID, Amount, TransactionType, Status, ReferenceNumber)
TransactionFees (FeeID, TransactionID, FeeAmount, FeeType, CollectedDate)
BankRevenue (RevenueID, Amount, RevenueType, CollectedDate)
```

```sql
CREATE PROCEDURE sp_ComplexTransfer
    @FromAccountID INT,
    @ToAccountID INT,
    @Amount DECIMAL(18,2),
    @TransferFee DECIMAL(18,2) = 5000.00,
    @BankAccountID INT = 999
AS
BEGIN
    DECLARE @ErrorMsg NVARCHAR(500);
    DECLARE @TransactionID INT;
    
    BEGIN TRY
        BEGIN TRANSACTION ComplexTransfer;
        
        -- Savepoint 1: Sau khi validate
        PRINT N'Bước 1: Kiểm tra tài khoản...';
        IF NOT EXISTS (SELECT 1 FROM Accounts WHERE AccountID = @FromAccountID)
        BEGIN
            THROW 50001, N'Tài khoản nguồn không tồn tại', 1;
        END
        SAVE TRANSACTION AfterValidation;
        PRINT N'✓ Validation hoàn tất';
        
        -- Savepoint 2: Sau khi trừ tiền chính
        PRINT N'Bước 2: Trừ tiền từ tài khoản nguồn...';
        UPDATE Accounts 
        SET Balance = Balance - @Amount 
        WHERE AccountID = @FromAccountID;
        
        IF @@ROWCOUNT = 0
        BEGIN
            ROLLBACK TRANSACTION AfterValidation;
            THROW 50002, N'Không thể trừ tiền từ tài khoản nguồn', 1;
        END
        SAVE TRANSACTION AfterDebit;
        PRINT N'✓ Đã trừ ' + CAST(@Amount AS NVARCHAR(50)) + ' VND';
        
        -- Savepoint 3: Sau khi trừ phí
        PRINT N'Bước 3: Trừ phí giao dịch...';
        UPDATE Accounts 
        SET Balance = Balance - @TransferFee 
        WHERE AccountID = @FromAccountID;
        
        IF (SELECT Balance FROM Accounts WHERE AccountID = @FromAccountID) < 0
        BEGIN
            ROLLBACK TRANSACTION AfterDebit;
            THROW 50003, N'Số dư không đủ để trả phí giao dịch', 1;
        END
        SAVE TRANSACTION AfterFeeDebit;
        PRINT N'✓ Đã trừ phí ' + CAST(@TransferFee AS NVARCHAR(50)) + ' VND';
        
        -- Savepoint 4: Sau khi cộng tiền cho người nhận
        PRINT N'Bước 4: Cộng tiền vào tài khoản đích...';
        UPDATE Accounts 
        SET Balance = Balance + @Amount 
        WHERE AccountID = @ToAccountID;
        
        IF @@ROWCOUNT = 0
        BEGIN
            ROLLBACK TRANSACTION AfterFeeDebit;
            THROW 50004, N'Không thể cộng tiền vào tài khoản đích', 1;
        END
        SAVE TRANSACTION AfterCredit;
        PRINT N'✓ Đã cộng ' + CAST(@Amount AS NVARCHAR(50)) + ' VND vào tài khoản đích';
        
        -- Savepoint 5: Sau khi ghi nhận doanh thu phí
        PRINT N'Bước 5: Ghi nhận doanh thu phí cho ngân hàng...';
        UPDATE Accounts 
        SET Balance = Balance + @TransferFee 
        WHERE AccountID = @BankAccountID;
        
        INSERT INTO BankRevenue (Amount, RevenueType, CollectedDate)
        VALUES (@TransferFee, 'TRANSFER_FEE', GETDATE());
        
        SAVE TRANSACTION AfterRevenueRecord;
        PRINT N'✓ Đã ghi nhận doanh thu phí';
        
        -- Savepoint 6: Sau khi ghi lịch sử
        PRINT N'Bước 6: Ghi lịch sử giao dịch...';
        INSERT INTO TransactionHistory (
            FromAccountID, ToAccountID, Amount, TransactionType, Status, ReferenceNumber
        )
        VALUES (
            @FromAccountID, @ToAccountID, @Amount, 'TRANSFER', 'COMPLETED',
            'TXN' + FORMAT(GETDATE(), 'yyyyMMddHHmmss')
        );
        
        SET @TransactionID = SCOPE_IDENTITY();
        
        INSERT INTO TransactionFees (TransactionID, FeeAmount, FeeType, CollectedDate)
        VALUES (@TransactionID, @TransferFee, 'TRANSFER', GETDATE());
        
        SAVE TRANSACTION AfterHistoryRecord;
        PRINT N'✓ Đã ghi lịch sử giao dịch';
        
        -- Commit tất cả
        COMMIT TRANSACTION ComplexTransfer;
        PRINT N'';
        PRINT N'========================================';
        PRINT N'GIAO DỊCH HOÀN TẤT THÀNH CÔNG!';
        PRINT N'========================================';
        
    END TRY
    BEGIN CATCH
        IF @@TRANCOUNT > 0
        BEGIN
            ROLLBACK TRANSACTION ComplexTransfer;
        END
        
        PRINT N'';
        PRINT N'========================================';
        PRINT N'GIAO DỊCH THẤT BẠI!';
        PRINT N'Lỗi: ' + ERROR_MESSAGE();
        PRINT N'========================================';
        
        THROW;
    END CATCH
END;
GO
```

Test stored procedure:

```sql
-- Tạo bảng BankRevenue và TransactionFees
CREATE TABLE BankRevenue (
    RevenueID INT PRIMARY KEY IDENTITY,
    Amount DECIMAL(18,2),
    RevenueType NVARCHAR(50),
    CollectedDate DATETIME DEFAULT GETDATE()
);

CREATE TABLE TransactionFees (
    FeeID INT PRIMARY KEY IDENTITY,
    TransactionID INT,
    FeeAmount DECIMAL(18,2),
    FeeType NVARCHAR(50),
    CollectedDate DATETIME DEFAULT GETDATE()
);

-- Tạo tài khoản ngân hàng
INSERT INTO Accounts (AccountID, CustomerID, AccountNumber, AccountType, Balance, Status)
VALUES (999, 1, 'BANK001', 'REVENUE', 0, 'ACTIVE');

-- Test giao dịch phức tạp
EXEC sp_ComplexTransfer 
    @FromAccountID = 1,
    @ToAccountID = 2,
    @Amount = 1000000.00,
    @TransferFee = 5000.00,
    @BankAccountID = 999;

/*
Kết quả:
Bước 1: Kiểm tra tài khoản...
✓ Validation hoàn tất
Bước 2: Trừ tiền từ tài khoản nguồn...
✓ Đã trừ 1000000.00 VND
Bước 3: Trừ phí giao dịch...
✓ Đã trừ phí 5000.00 VND
Bước 4: Cộng tiền vào tài khoản đích...
✓ Đã cộng 1000000.00 VND vào tài khoản đích
Bước 5: Ghi nhận doanh thu phí cho ngân hàng...
✓ Đã ghi nhận doanh thu phí
Bước 6: Ghi lịch sử giao dịch...
✓ Đã ghi lịch sử giao dịch

========================================
GIAO DỊCH HOÀN TẤT THÀNH CÔNG!
========================================
*/

-- Kiểm tra kết quả
SELECT AccountID, Balance FROM Accounts WHERE AccountID IN (1, 2, 999);
/*
AccountID | Balance
----------|------------
1         | 6995000.00   (8,000,000 - 1,000,000 - 5,000)
2         | 8000000.00   (7,000,000 + 1,000,000)
999       | 5000.00      (0 + 5,000)
*/
```
