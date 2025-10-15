-- =============================================
-- THỰC HÀNH TRANSACTION TRONG MYSQL
-- =============================================



-- =============================================
-- 1. DEMO TRANSACTION CƠ BẢN
-- =============================================

-- Xem dữ liệu TRƯỚC transaction
SELECT 'TRƯỚC Transaction:' AS Status;
SELECT AccountID, AccountNumber, Balance FROM Accounts;
-- Kết quả mong đợi: AccountID=1 Balance=10000000, AccountID=2 Balance=5000000

-- BEGIN TRANSACTION và UPDATE
START TRANSACTION;

UPDATE Accounts 
SET Balance = Balance - 2000000 
WHERE AccountID = 1;

UPDATE Accounts 
SET Balance = Balance + 2000000 
WHERE AccountID = 2;

-- Xem dữ liệu TRONG transaction (chưa commit)
SELECT 'TRONG Transaction (chưa commit):' AS Status;
SELECT AccountID, AccountNumber, Balance FROM Accounts;
-- Kết quả mong đợi: AccountID=1 Balance=8000000, AccountID=2 Balance=7000000

-- COMMIT TRANSACTION
COMMIT;

-- Xem dữ liệu SAU khi COMMIT
SELECT 'SAU khi COMMIT:' AS Status;
SELECT AccountID, AccountNumber, Balance FROM Accounts;
-- Kết quả mong đợi: AccountID=1 Balance=8000000, AccountID=2 Balance=7000000 (thay đổi đã được lưu)

-- =============================================
-- 2. DEMO ROLLBACK TRANSACTION
-- =============================================

-- Xem dữ liệu trước rollback demo
SELECT 'TRƯỚC Rollback Demo:' AS Status;
SELECT AccountID, AccountNumber, Balance FROM Accounts;
-- Kết quả mong đợi: AccountID=1 Balance=8000000, AccountID=2 Balance=7000000

-- Bắt đầu transaction
START TRANSACTION;

UPDATE Accounts 
SET Balance = Balance - 1000000 
WHERE AccountID = 1;

UPDATE Accounts 
SET Balance = Balance + 1000000 
WHERE AccountID = 2;

-- Xem dữ liệu trong transaction
SELECT 'TRONG Transaction (sẽ rollback):' AS Status;
SELECT AccountID, AccountNumber, Balance FROM Accounts;
-- Kết quả mong đợi: AccountID=1 Balance=7000000, AccountID=2 Balance=8000000

-- ROLLBACK thay vì COMMIT
ROLLBACK;

-- Xem dữ liệu sau khi ROLLBACK
SELECT 'SAU khi ROLLBACK:' AS Status;
SELECT AccountID, AccountNumber, Balance FROM Accounts;
-- Kết quả mong đợi: AccountID=1 Balance=8000000, AccountID=2 Balance=7000000 (quay về trạng thái ban đầu)

-- =============================================
-- 3. DEMO SAVEPOINT
-- =============================================

-- Bắt đầu transaction với savepoint
START TRANSACTION;

-- Bước 1: Trừ tiền tài khoản 1
UPDATE Accounts 
SET Balance = Balance - 500000 
WHERE AccountID = 1;

-- Tạo savepoint sau bước 1
SAVEPOINT step1;

-- Bước 2: Cộng tiền tài khoản 2
UPDATE Accounts 
SET Balance = Balance + 500000 
WHERE AccountID = 2;

-- Xem dữ liệu sau bước 2
SELECT 'Sau bước 2 (có savepoint):' AS Status;
SELECT AccountID, AccountNumber, Balance FROM Accounts;
-- Kết quả mong đợi: AccountID=1 Balance=7500000, AccountID=2 Balance=7500000

-- Rollback về savepoint (chỉ hủy bước 2)
ROLLBACK TO step1;

-- Xem dữ liệu sau khi rollback về savepoint
SELECT 'Sau rollback về savepoint:' AS Status;
SELECT AccountID, AccountNumber, Balance FROM Accounts;
-- Kết quả mong đợi: AccountID=1 Balance=7500000, AccountID=2 Balance=7000000 (chỉ bước 1 được giữ lại)

-- Commit những thay đổi còn lại
COMMIT;

-- =============================================
-- 4. DEMO CHUYỂN TIỀN AN TOÀN (TÌNH HUỐNG THỰC TẾ)
-- =============================================

-- Procedure chuyển tiền an toàn
DELIMITER //
CREATE PROCEDURE ChuyenTien(
    IN p_from_account INT,
    IN p_to_account INT, 
    IN p_amount DECIMAL(18,2)
)
BEGIN
    DECLARE v_balance DECIMAL(18,2);
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SELECT 'Lỗi: Transaction đã được rollback' AS Result;
    END;
    
    START TRANSACTION;
    
    -- Kiểm tra số dư
    SELECT Balance INTO v_balance 
    FROM Accounts 
    WHERE AccountID = p_from_account;
    
    IF v_balance < p_amount THEN
        SELECT 'Lỗi: Số dư không đủ' AS Result;
        ROLLBACK;
    ELSE
        -- Trừ tiền tài khoản nguồn
        UPDATE Accounts 
        SET Balance = Balance - p_amount 
        WHERE AccountID = p_from_account;
        
        -- Cộng tiền tài khoản đích
        UPDATE Accounts 
        SET Balance = Balance + p_amount 
        WHERE AccountID = p_to_account;
        
        -- Ghi log giao dịch
        INSERT INTO TransactionHistory 
        (FromAccountID, ToAccountID, Amount, TransactionType, Status, Description, ReferenceNumber)
        VALUES 
        (p_from_account, p_to_account, p_amount, 'TRANSFER', 'SUCCESS', 
         CONCAT('Chuyển tiền từ ACC', LPAD(p_from_account, 3, '0'), ' sang ACC', LPAD(p_to_account, 3, '0')),
         CONCAT('TXN', DATE_FORMAT(NOW(), '%Y%m%d%H%i%s')));
        
        COMMIT;
        SELECT 'Thành công: Chuyển tiền hoàn tất' AS Result;
    END IF;
END //
DELIMITER ;

-- =============================================
-- 5. TEST CHUYỂN TIỀN AN TOÀN
-- =============================================

-- Xem số dư trước khi chuyển
SELECT 'TRƯỚC khi chuyển tiền an toàn:' AS Status;
SELECT AccountID, AccountNumber, Balance FROM Accounts;
-- Kết quả mong đợi: AccountID=1 Balance=7500000, AccountID=2 Balance=7000000

-- Chuyển 1,000,000 VND từ tài khoản 1 sang tài khoản 2
CALL ChuyenTien(1, 2, 1000000);
-- Kết quả mong đợi: 'Thành công: Chuyển tiền hoàn tất'

-- Xem số dư sau khi chuyển
SELECT 'SAU khi chuyển tiền an toàn:' AS Status;
SELECT AccountID, AccountNumber, Balance FROM Accounts;
-- Kết quả mong đợi: AccountID=1 Balance=6500000, AccountID=2 Balance=8000000

-- Xem lịch sử giao dịch
SELECT 'Lịch sử giao dịch:' AS Status;
SELECT * FROM TransactionHistory;

-- =============================================
-- 6. TEST TRƯỜNG HỢP LỖI (SỐ DƯ KHÔNG ĐỦ)
-- =============================================

-- Thử chuyển số tiền lớn hơn số dư
CALL ChuyenTien(2, 1, 50000000);
-- Kết quả mong đợi: 'Lỗi: Số dư không đủ'

-- Kiểm tra số dư không thay đổi
SELECT 'Sau khi thử chuyển tiền vượt số dư:' AS Status;
SELECT AccountID, AccountNumber, Balance FROM Accounts;
-- Kết quả mong đợi: AccountID=1 Balance=6500000, AccountID=2 Balance=8000000 (không thay đổi)