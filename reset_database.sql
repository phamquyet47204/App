-- Reset và tạo lại database
DROP DATABASE IF EXISTS BankingSystem;
CREATE DATABASE BankingSystem;
USE BankingSystem;

-- Tạo bảng Customers
CREATE TABLE Customers (
    CustomerID INT PRIMARY KEY,
    CustomerName VARCHAR(100) NOT NULL,
    Email VARCHAR(100),
    Phone VARCHAR(20),
    Address VARCHAR(200),
    CreatedDate DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Tạo bảng Accounts
CREATE TABLE Accounts (
    AccountID INT PRIMARY KEY,
    CustomerID INT,
    AccountNumber VARCHAR(20) UNIQUE NOT NULL,
    AccountType VARCHAR(50) NOT NULL,
    Balance DECIMAL(18,2) NOT NULL DEFAULT 0,
    Status VARCHAR(20) NOT NULL DEFAULT 'ACTIVE',
    CreatedDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)
);

-- Tạo bảng TransactionHistory
CREATE TABLE TransactionHistory (
    TransactionID INT PRIMARY KEY AUTO_INCREMENT,
    FromAccountID INT,
    ToAccountID INT,
    Amount DECIMAL(18,2) NOT NULL,
    TransactionType VARCHAR(50) NOT NULL,
    TransactionDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    Status VARCHAR(20) NOT NULL,
    Description VARCHAR(500),
    ReferenceNumber VARCHAR(50) UNIQUE
);

-- Insert dữ liệu
INSERT INTO Customers (CustomerID, CustomerName, Email, Phone, Address) VALUES 
(1, 'Nguyễn Văn An', 'an@email.com', '0901234567', '123 Lê Lợi, Q1, TP.HCM'),
(2, 'Trần Thị Bình', 'binh@email.com', '0902345678', '456 Nguyễn Huệ, Q1, TP.HCM');

INSERT INTO Accounts (AccountID, CustomerID, AccountNumber, AccountType, Balance, Status) VALUES 
(1, 1, 'ACC001', 'SAVINGS', 10000000.00, 'ACTIVE'),
(2, 2, 'ACC002', 'CHECKING', 5000000.00, 'ACTIVE');

-- Kiểm tra dữ liệu
SELECT 'TRƯỚC khi chuyển tiền:' AS Status;
SELECT AccountID, AccountNumber, CustomerID, Balance FROM Accounts;