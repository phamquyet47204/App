-- ============================================================================
-- SQL Import Script for Students
-- File: import_students.sql
-- Description: Import sample student data into University Management System
-- Usage: mysql -u username -p database_name < import_students.sql
-- ============================================================================

-- Disable foreign key checks temporarily
SET FOREIGN_KEY_CHECKS = 0;
SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

-- ============================================================================
-- STEP 1: Ensure required master data exists (Departments, Majors, Classes)
-- ============================================================================

-- Insert Departments (if not exists)
INSERT IGNORE INTO `core_department` (`departmentId`, `departmentCode`, `departmentName`, `status`, `createdAt`) VALUES
('DEPT001', 'IT', 'Information Technology', 'active', NOW()),
('DEPT002', 'BUS', 'Business Administration', 'active', NOW()),
('DEPT003', 'ENG', 'Engineering', 'active', NOW());

-- Insert Majors (if not exists)
INSERT IGNORE INTO `core_major` (`majorId`, `majorCode`, `majorName`, `department_id`, `durationYears`, `totalCredits`, `status`) VALUES
('MAJ001', 'SE', 'Software Engineering', 'DEPT001', 4, 140, 1),
('MAJ002', 'CS', 'Computer Science', 'DEPT001', 4, 140, 1),
('MAJ003', 'BA', 'Business Administration', 'DEPT002', 4, 140, 1),
('MAJ004', 'CE', 'Civil Engineering', 'DEPT003', 4, 140, 1);

-- Ensure Teachers exist (if not exists)
-- Note: Teachers must exist before creating CourseClasses
INSERT IGNORE INTO `core_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`, `full_name`, `phone`, `user_type`, `status`, `created_at`, `updated_at`) VALUES
(2, 'pbkdf2_sha256$870000$nJyPhhJGlR4d0a0EBwh9Nt$+nlop5f0lMllJWPAxQIZRJXswgTQLZu+dmfd8CQL5Hs=', NULL, 0, 'teacher1', '', '', 'teacher1@test.com', 0, 1, NOW(), 'Nguyen Van A', '121212', 'teacher', 'active', NOW(), NOW()),
(3, 'pbkdf2_sha256$870000$ivDk7kTay9EvbYGLT7EiS6$0ZAQbZma0gHPsCzKhq7DIyyjx5XxCcil3Eh+huPRtIg=', NULL, 0, 'teacher2', '', '', 'teacher2@test.com', 0, 1, NOW(), 'Tran Thi B', NULL, 'teacher', 'active', NOW(), NOW()),
(4, 'pbkdf2_sha256$870000$nJyPhhJGlR4d0a0EBwh9Nt$+nlop5f0lMllJWPAxQIZRJXswgTQLZu+dmfd8CQL5Hs=', NULL, 0, 'teacher3', '', '', 'teacher3@test.com', 0, 1, NOW(), 'Prof. Mike Johnson', NULL, 'teacher', 'active', NOW(), NOW()),
(5, 'pbkdf2_sha256$870000$ivDk7kTay9EvbYGLT7EiS6$0ZAQbZma0gHPsCzKhq7DIyyjx5XxCcil3Eh+huPRtIg=', NULL, 0, 'teacher4', '', '', 'teacher4@test.com', 0, 1, NOW(), 'Dr. Sarah Wilson', NULL, 'teacher', 'active', NOW(), NOW());

INSERT IGNORE INTO `core_teacher` (`user_id`, `teacherId`, `teacherCode`, `department_id`, `position`, `hireDate`) VALUES
(2, 'T001', 'IT001', 'DEPT001', 'Lecturer', '2020-01-01'),
(3, 'T002', 'IT002', 'DEPT001', 'Lecturer', '2020-01-01'),
(4, 'T003', 'BUS001', 'DEPT002', 'Professor', '2020-01-01'),
(5, 'T004', 'ENG001', 'DEPT003', 'Associate Professor', '2020-01-01');

-- Insert Student Classes (if not exists)
-- Note: Requires existing majors and advisor teacher (assuming teacher with user_id=2)
INSERT IGNORE INTO `core_studentclass` (`classId`, `classCode`, `className`, `academicYear`, `maxStudents`, `currentStudents`, `status`, `major_id`, `advisorTeacher_id`) VALUES
('CL001', 'SE2024A', 'Software Engineering 2024A', '2024-2025', 30, 0, 1, 'MAJ001', 2),
('CL002', 'SE2024B', 'Software Engineering 2024B', '2024-2025', 30, 0, 1, 'MAJ001', 2),
('CL003', 'CS2024A', 'Computer Science 2024A', '2024-2025', 30, 0, 1, 'MAJ002', 2),
('CL004', 'BA2024A', 'Business Administration 2024A', '2024-2025', 30, 0, 1, 'MAJ003', 2),
('CL005', 'CE2024A', 'Civil Engineering 2024A', '2024-2025', 30, 0, 1, 'MAJ004', 2);

-- ============================================================================
-- STEP 2: Insert User records (students)
-- Password hash for 'python123': pbkdf2_sha256$870000$... (will generate unique salts)
-- For simplicity, using a consistent hash - in production, generate unique hashes
-- ============================================================================

-- Get the next available user ID (adjust based on your current max user_id)
SET @next_user_id = (SELECT COALESCE(MAX(id), 0) + 1 FROM core_user);

-- Insert Users for Students
-- Note: Adjust user_id values based on your existing data
INSERT INTO `core_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`, `full_name`, `phone`, `user_type`, `status`, `created_at`, `updated_at`) VALUES
-- Students 1-10
(@next_user_id + 0, 'pbkdf2_sha256$870000$cIDG5f0G1oXiio1msBINYk$Tl8uMAI0xGE8d7F5SdwZvg/h6n6s3CvYPD7DClchd7s=', NULL, 0, 'student1', '', '', 'student1@test.com', 0, 1, NOW(), 'Nguyen Van An', '0321000001', 'student', 'active', NOW(), NOW()),
(@next_user_id + 1, 'pbkdf2_sha256$870000$cIDG5f0G1oXiio1msBINYk$Tl8uMAI0xGE8d7F5SdwZvg/h6n6s3CvYPD7DClchd7s=', NULL, 0, 'student2', '', '', 'student2@test.com', 0, 1, NOW(), 'Tran Thi Binh', '0321000002', 'student', 'active', NOW(), NOW()),
(@next_user_id + 2, 'pbkdf2_sha256$870000$cIDG5f0G1oXiio1msBINYk$Tl8uMAI0xGE8d7F5SdwZvg/h6n6s3CvYPD7DClchd7s=', NULL, 0, 'student3', '', '', 'student3@test.com', 0, 1, NOW(), 'Le Van Cuong', '0321000003', 'student', 'active', NOW(), NOW()),
(@next_user_id + 3, 'pbkdf2_sha256$870000$cIDG5f0G1oXiio1msBINYk$Tl8uMAI0xGE8d7F5SdwZvg/h6n6s3CvYPD7DClchd7s=', NULL, 0, 'student4', '', '', 'student4@test.com', 0, 1, NOW(), 'Pham Thi Dung', '0321000004', 'student', 'active', NOW(), NOW()),
(@next_user_id + 4, 'pbkdf2_sha256$870000$cIDG5f0G1oXiio1msBINYk$Tl8uMAI0xGE8d7F5SdwZvg/h6n6s3CvYPD7DClchd7s=', NULL, 0, 'student5', '', '', 'student5@test.com', 0, 1, NOW(), 'Hoang Van Em', '0321000005', 'student', 'active', NOW(), NOW()),
(@next_user_id + 5, 'pbkdf2_sha256$870000$cIDG5f0G1oXiio1msBINYk$Tl8uMAI0xGE8d7F5SdwZvg/h6n6s3CvYPD7DClchd7s=', NULL, 0, 'student6', '', '', 'student6@test.com', 0, 1, NOW(), 'Vu Thi Phuong', '0321000006', 'student', 'active', NOW(), NOW()),
(@next_user_id + 6, 'pbkdf2_sha256$870000$cIDG5f0G1oXiio1msBINYk$Tl8uMAI0xGE8d7F5SdwZvg/h6n6s3CvYPD7DClchd7s=', NULL, 0, 'student7', '', '', 'student7@test.com', 0, 1, NOW(), 'Dang Van Giang', '0321000007', 'student', 'active', NOW(), NOW()),
(@next_user_id + 7, 'pbkdf2_sha256$870000$cIDG5f0G1oXiio1msBINYk$Tl8uMAI0xGE8d7F5SdwZvg/h6n6s3CvYPD7DClchd7s=', NULL, 0, 'student8', '', '', 'student8@test.com', 0, 1, NOW(), 'Bui Thi Hoa', '0321000008', 'student', 'active', NOW(), NOW()),
(@next_user_id + 8, 'pbkdf2_sha256$870000$cIDG5f0G1oXiio1msBINYk$Tl8uMAI0xGE8d7F5SdwZvg/h6n6s3CvYPD7DClchd7s=', NULL, 0, 'student9', '', '', 'student9@test.com', 0, 1, NOW(), 'Dao Van Hung', '0321000009', 'student', 'active', NOW(), NOW()),
(@next_user_id + 9, 'pbkdf2_sha256$870000$cIDG5f0G1oXiio1msBINYk$Tl8uMAI0xGE8d7F5SdwZvg/h6n6s3CvYPD7DClchd7s=', NULL, 0, 'student10', '', '', 'student10@test.com', 0, 1, NOW(), 'Do Thi Khanh', '0321000010', 'student', 'active', NOW(), NOW()),
-- Students 11-20
(@next_user_id + 10, 'pbkdf2_sha256$870000$cIDG5f0G1oXiio1msBINYk$Tl8uMAI0xGE8d7F5SdwZvg/h6n6s3CvYPD7DClchd7s=', NULL, 0, 'student11', '', '', 'student11@test.com', 0, 1, NOW(), 'Ngo Van Long', '0321000011', 'student', 'active', NOW(), NOW()),
(@next_user_id + 11, 'pbkdf2_sha256$870000$cIDG5f0G1oXiio1msBINYk$Tl8uMAI0xGE8d7F5SdwZvg/h6n6s3CvYPD7DClchd7s=', NULL, 0, 'student12', '', '', 'student12@test.com', 0, 1, NOW(), 'Ly Thi Mai', '0321000012', 'student', 'active', NOW(), NOW()),
(@next_user_id + 12, 'pbkdf2_sha256$870000$cIDG5f0G1oXiio1msBINYk$Tl8uMAI0xGE8d7F5SdwZvg/h6n6s3CvYPD7DClchd7s=', NULL, 0, 'student13', '', '', 'student13@test.com', 0, 1, NOW(), 'Kim Van Nam', '0321000013', 'student', 'active', NOW(), NOW()),
(@next_user_id + 13, 'pbkdf2_sha256$870000$cIDG5f0G1oXiio1msBINYk$Tl8uMAI0xGE8d7F5SdwZvg/h6n6s3CvYPD7DClchd7s=', NULL, 0, 'student14', '', '', 'student14@test.com', 0, 1, NOW(), 'Truong Thi Oanh', '0321000014', 'student', 'active', NOW(), NOW()),
(@next_user_id + 14, 'pbkdf2_sha256$870000$cIDG5f0G1oXiio1msBINYk$Tl8uMAI0xGE8d7F5SdwZvg/h6n6s3CvYPD7DClchd7s=', NULL, 0, 'student15', '', '', 'student15@test.com', 0, 1, NOW(), 'Lam Van Phuc', '0321000015', 'student', 'active', NOW(), NOW()),
(@next_user_id + 15, 'pbkdf2_sha256$870000$cIDG5f0G1oXiio1msBINYk$Tl8uMAI0xGE8d7F5SdwZvg/h6n6s3CvYPD7DClchd7s=', NULL, 0, 'student16', '', '', 'student16@test.com', 0, 1, NOW(), 'Cao Thi Quyen', '0321000016', 'student', 'active', NOW(), NOW()),
(@next_user_id + 16, 'pbkdf2_sha256$870000$cIDG5f0G1oXiio1msBINYk$Tl8uMAI0xGE8d7F5SdwZvg/h6n6s3CvYPD7DClchd7s=', NULL, 0, 'student17', '', '', 'student17@test.com', 0, 1, NOW(), 'Phan Van Rong', '0321000017', 'student', 'active', NOW(), NOW()),
(@next_user_id + 17, 'pbkdf2_sha256$870000$cIDG5f0G1oXiio1msBINYk$Tl8uMAI0xGE8d7F5SdwZvg/h6n6s3CvYPD7DClchd7s=', NULL, 0, 'student18', '', '', 'student18@test.com', 0, 1, NOW(), 'Tran Thi Son', '0321000018', 'student', 'active', NOW(), NOW()),
(@next_user_id + 18, 'pbkdf2_sha256$870000$cIDG5f0G1oXiio1msBINYk$Tl8uMAI0xGE8d7F5SdwZvg/h6n6s3CvYPD7DClchd7s=', NULL, 0, 'student19', '', '', 'student19@test.com', 0, 1, NOW(), 'Le Van Tam', '0321000019', 'student', 'active', NOW(), NOW()),
(@next_user_id + 19, 'pbkdf2_sha256$870000$cIDG5f0G1oXiio1msBINYk$Tl8uMAI0xGE8d7F5SdwZvg/h6n6s3CvYPD7DClchd7s=', NULL, 0, 'student20', '', '', 'student20@test.com', 0, 1, NOW(), 'Vo Thi Uyen', '0321000020', 'student', 'active', NOW(), NOW()),
-- Additional students 21-30
(@next_user_id + 20, 'pbkdf2_sha256$870000$cIDG5f0G1oXiio1msBINYk$Tl8uMAI0xGE8d7F5SdwZvg/h6n6s3CvYPD7DClchd7s=', NULL, 0, 'student21', '', '', 'student21@test.com', 0, 1, NOW(), 'Nguyen Van Vinh', '0321000021', 'student', 'active', NOW(), NOW()),
(@next_user_id + 21, 'pbkdf2_sha256$870000$cIDG5f0G1oXiio1msBINYk$Tl8uMAI0xGE8d7F5SdwZvg/h6n6s3CvYPD7DClchd7s=', NULL, 0, 'student22', '', '', 'student22@test.com', 0, 1, NOW(), 'Hoang Thi Xuan', '0321000022', 'student', 'active', NOW(), NOW()),
(@next_user_id + 22, 'pbkdf2_sha256$870000$cIDG5f0G1oXiio1msBINYk$Tl8uMAI0xGE8d7F5SdwZvg/h6n6s3CvYPD7DClchd7s=', NULL, 0, 'student23', '', '', 'student23@test.com', 0, 1, NOW(), 'Pham Van Yen', '0321000023', 'student', 'active', NOW(), NOW()),
(@next_user_id + 23, 'pbkdf2_sha256$870000$cIDG5f0G1oXiio1msBINYk$Tl8uMAI0xGE8d7F5SdwZvg/h6n6s3CvYPD7DClchd7s=', NULL, 0, 'student24', '', '', 'student24@test.com', 0, 1, NOW(), 'Duong Thi An', '0321000024', 'student', 'active', NOW(), NOW()),
(@next_user_id + 24, 'pbkdf2_sha256$870000$cIDG5f0G1oXiio1msBINYk$Tl8uMAI0xGE8d7F5SdwZvg/h6n6s3CvYPD7DClchd7s=', NULL, 0, 'student25', '', '', 'student25@test.com', 0, 1, NOW(), 'Tran Van Bao', '0321000025', 'student', 'active', NOW(), NOW()),
(@next_user_id + 25, 'pbkdf2_sha256$870000$cIDG5f0G1oXiio1msBINYk$Tl8uMAI0xGE8d7F5SdwZvg/h6n6s3CvYPD7DClchd7s=', NULL, 0, 'student26', '', '', 'student26@test.com', 0, 1, NOW(), 'Le Thi Cam', '0321000026', 'student', 'active', NOW(), NOW()),
(@next_user_id + 26, 'pbkdf2_sha256$870000$cIDG5f0G1oXiio1msBINYk$Tl8uMAI0xGE8d7F5SdwZvg/h6n6s3CvYPD7DClchd7s=', NULL, 0, 'student27', '', '', 'student27@test.com', 0, 1, NOW(), 'Pham Van Duc', '0321000027', 'student', 'active', NOW(), NOW()),
(@next_user_id + 27, 'pbkdf2_sha256$870000$cIDG5f0G1oXiio1msBINYk$Tl8uMAI0xGE8d7F5SdwZvg/h6n6s3CvYPD7DClchd7s=', NULL, 0, 'student28', '', '', 'student28@test.com', 0, 1, NOW(), 'Nguyen Thi Em', '0321000028', 'student', 'active', NOW(), NOW()),
(@next_user_id + 28, 'pbkdf2_sha256$870000$cIDG5f0G1oXiio1msBINYk$Tl8uMAI0xGE8d7F5SdwZvg/h6n6s3CvYPD7DClchd7s=', NULL, 0, 'student29', '', '', 'student29@test.com', 0, 1, NOW(), 'Tran Van Phong', '0321000029', 'student', 'active', NOW(), NOW()),
(@next_user_id + 29, 'pbkdf2_sha256$870000$cIDG5f0G1oXiio1msBINYk$Tl8uMAI0xGE8d7F5SdwZvg/h6n6s3CvYPD7DClchd7s=', NULL, 0, 'student30', '', '', 'student30@test.com', 0, 1, NOW(), 'Hoang Thi Quynh', '0321000030', 'student', 'active', NOW(), NOW());

-- ============================================================================
-- STEP 3: Insert Student records
-- Note: user_id must match the user.id values from STEP 2
-- ============================================================================

-- Use variables to store user IDs (adjust based on your starting user_id)
SET @user_student1 = @next_user_id + 0;
SET @user_student2 = @next_user_id + 1;
SET @user_student3 = @next_user_id + 2;
SET @user_student4 = @next_user_id + 3;
SET @user_student5 = @next_user_id + 4;
SET @user_student6 = @next_user_id + 5;
SET @user_student7 = @next_user_id + 6;
SET @user_student8 = @next_user_id + 7;
SET @user_student9 = @next_user_id + 8;
SET @user_student10 = @next_user_id + 9;
SET @user_student11 = @next_user_id + 10;
SET @user_student12 = @next_user_id + 11;
SET @user_student13 = @next_user_id + 12;
SET @user_student14 = @next_user_id + 13;
SET @user_student15 = @next_user_id + 14;
SET @user_student16 = @next_user_id + 15;
SET @user_student17 = @next_user_id + 16;
SET @user_student18 = @next_user_id + 17;
SET @user_student19 = @next_user_id + 18;
SET @user_student20 = @next_user_id + 19;
SET @user_student21 = @next_user_id + 20;
SET @user_student22 = @next_user_id + 21;
SET @user_student23 = @next_user_id + 22;
SET @user_student24 = @next_user_id + 23;
SET @user_student25 = @next_user_id + 24;
SET @user_student26 = @next_user_id + 25;
SET @user_student27 = @next_user_id + 26;
SET @user_student28 = @next_user_id + 27;
SET @user_student29 = @next_user_id + 28;
SET @user_student30 = @next_user_id + 29;

INSERT INTO `core_student` (`user_id`, `studentId`, `studentCode`, `dateOfBirth`, `gender`, `enrollmentYear`, `gpa`, `totalCredits`, `studentClass_id`) VALUES
-- Students 1-10 (Distributed across classes)
(@user_student1, 'S001', 'SE001', '2002-01-15', 'male', 2024, 0.0, 0, 'CL001'),
(@user_student2, 'S002', 'SE002', '2002-02-20', 'female', 2024, 0.0, 0, 'CL001'),
(@user_student3, 'S003', 'SE003', '2002-03-10', 'male', 2024, 0.0, 0, 'CL002'),
(@user_student4, 'S004', 'SE004', '2002-04-25', 'female', 2024, 0.0, 0, 'CL002'),
(@user_student5, 'S005', 'SE005', '2002-05-12', 'male', 2024, 0.0, 0, 'CL003'),
(@user_student6, 'S006', 'SE006', '2002-06-18', 'female', 2024, 0.0, 0, 'CL003'),
(@user_student7, 'S007', 'SE007', '2002-07-05', 'male', 2024, 0.0, 0, 'CL004'),
(@user_student8, 'S008', 'SE008', '2002-08-22', 'female', 2024, 0.0, 0, 'CL004'),
(@user_student9, 'S009', 'SE009', '2002-09-30', 'male', 2024, 0.0, 0, 'CL001'),
(@user_student10, 'S010', 'SE010', '2002-10-08', 'female', 2024, 0.0, 0, 'CL002'),
-- Students 11-20
(@user_student11, 'S011', 'SE011', '2002-11-14', 'male', 2024, 0.0, 0, 'CL003'),
(@user_student12, 'S012', 'SE012', '2002-12-01', 'female', 2024, 0.0, 0, 'CL004'),
(@user_student13, 'S013', 'SE013', '2003-01-16', 'male', 2024, 0.0, 0, 'CL001'),
(@user_student14, 'S014', 'SE014', '2003-02-23', 'female', 2024, 0.0, 0, 'CL002'),
(@user_student15, 'S015', 'SE015', '2003-03-11', 'male', 2024, 0.0, 0, 'CL003'),
(@user_student16, 'S016', 'SE016', '2003-04-28', 'female', 2024, 0.0, 0, 'CL004'),
(@user_student17, 'S017', 'SE017', '2003-05-06', 'male', 2024, 0.0, 0, 'CL001'),
(@user_student18, 'S018', 'SE018', '2003-06-13', 'female', 2024, 0.0, 0, 'CL002'),
(@user_student19, 'S019', 'SE019', '2003-07-20', 'male', 2024, 0.0, 0, 'CL003'),
(@user_student20, 'S020', 'SE020', '2003-08-27', 'female', 2024, 0.0, 0, 'CL004'),
-- Students 21-30
(@user_student21, 'S021', 'SE021', '2003-09-04', 'male', 2024, 0.0, 0, 'CL001'),
(@user_student22, 'S022', 'SE022', '2003-10-11', 'female', 2024, 0.0, 0, 'CL002'),
(@user_student23, 'S023', 'SE023', '2003-11-18', 'male', 2024, 0.0, 0, 'CL003'),
(@user_student24, 'S024', 'SE024', '2003-12-25', 'female', 2024, 0.0, 0, 'CL004'),
(@user_student25, 'S025', 'SE025', '2004-01-01', 'male', 2024, 0.0, 0, 'CL001'),
(@user_student26, 'S026', 'SE026', '2004-02-08', 'female', 2024, 0.0, 0, 'CL002'),
(@user_student27, 'S027', 'SE027', '2004-03-15', 'male', 2024, 0.0, 0, 'CL003'),
(@user_student28, 'S028', 'SE028', '2004-04-22', 'female', 2024, 0.0, 0, 'CL004'),
(@user_student29, 'S029', 'SE029', '2004-05-29', 'male', 2024, 0.0, 0, 'CL001'),
(@user_student30, 'S030', 'SE030', '2004-06-06', 'female', 2024, 0.0, 0, 'CL002');

-- ============================================================================
-- STEP 4: Update StudentClass currentStudents count
-- ============================================================================

UPDATE `core_studentclass` SET `currentStudents` = (
    SELECT COUNT(*) 
    FROM `core_student` 
    WHERE `core_student`.`studentClass_id` = `core_studentclass`.`classId`
);

-- ============================================================================
-- STEP 5: Create Semester (if not exists)
-- ============================================================================

INSERT IGNORE INTO `core_semester` (`semesterId`, `semesterCode`, `semesterName`, `academicYear_id`, `startDate`, `endDate`, `registrationStart`, `registrationEnd`, `status`) VALUES
('SEM001', '2024-1', 'Semester 1 - 2024', (SELECT yearId FROM core_academicyear WHERE yearCode = '2024-2025' LIMIT 1), 
 '2024-09-01', '2024-12-31', 
 DATE_SUB(NOW(), INTERVAL 7 DAY), 
 DATE_ADD(NOW(), INTERVAL 30 DAY), 
 'active');

-- Create Academic Year if not exists
INSERT IGNORE INTO `core_academicyear` (`yearId`, `yearCode`, `yearName`, `startYear`, `endYear`) VALUES
('AY001', '2024-2025', 'Academic Year 2024-2025', 2024, 2025);

-- Update semester with academic year
UPDATE `core_semester` SET `academicYear_id` = 'AY001' WHERE `semesterId` = 'SEM001' AND `academicYear_id` IS NULL;

-- ============================================================================
-- STEP 6: Create Subjects (if not exists)
-- ============================================================================

INSERT IGNORE INTO `core_subject` (`subjectId`, `subjectCode`, `subjectName`, `credits`, `theoryHours`, `practiceHours`, `status`, `department_id`) VALUES
('SUB001', 'CS101', 'Programming Fundamentals', 3, 30, 30, 'active', 'DEPT001'),
('SUB002', 'CS102', 'Data Structures', 3, 30, 30, 'active', 'DEPT001'),
('SUB003', 'CS103', 'Database Systems', 3, 30, 30, 'active', 'DEPT001'),
('SUB004', 'CS104', 'Web Development', 3, 30, 30, 'active', 'DEPT001'),
('SUB005', 'CS201', 'Advanced Programming', 4, 45, 30, 'active', 'DEPT001'),
('SUB006', 'CS202', 'Software Engineering', 4, 45, 30, 'active', 'DEPT001'),
('SUB007', 'BA101', 'Introduction to Business', 3, 30, 0, 'active', 'DEPT002'),
('SUB008', 'BA102', 'Business Management', 3, 30, 0, 'active', 'DEPT002'),
('SUB009', 'ENG101', 'Engineering Principles', 3, 30, 30, 'active', 'DEPT003'),
('SUB010', 'ENG102', 'Structural Analysis', 3, 30, 30, 'active', 'DEPT003');

-- ============================================================================
-- STEP 7: Create Course Classes with Full Schedule (Date & Time)
-- ============================================================================

-- Calculate base date (Monday of current week)
SET @base_monday = DATE_SUB(CURDATE(), INTERVAL WEEKDAY(CURDATE()) DAY);

-- Course Classes with Schedule (DateTime format: YYYY-MM-DD HH:MM:SS)
-- Schedule format: Day of week + specific time
-- Example: Monday 7:00 AM = base_monday + 0 days + 07:00:00

INSERT IGNORE INTO `core_courseclass` 
(`courseClassId`, `courseCode`, `courseName`, `room`, `schedule`, `maxStudents`, `currentStudents`, `status`, `semester_id`, `subject_id`, `teacher_id`) 
VALUES
-- Monday classes (7:00-9:00)
('CC001', 'CS101-01', 'Programming Fundamentals - Class 1', 'Room 101', 
 CONCAT(@base_monday, ' 07:00:00'), 30, 0, 1, 'SEM001', 'SUB001', 
 (SELECT user_id FROM core_teacher WHERE teacherCode = 'IT001' LIMIT 1)),
 
('CC002', 'CS102-01', 'Data Structures - Class 1', 'Room 102', 
 CONCAT(@base_monday, ' 09:00:00'), 30, 0, 1, 'SEM001', 'SUB002',
 (SELECT user_id FROM core_teacher WHERE teacherCode = 'IT002' LIMIT 1)),

-- Tuesday classes (7:00-9:00, 9:00-11:00)
('CC003', 'CS103-01', 'Database Systems - Class 1', 'Room 103', 
 CONCAT(DATE_ADD(@base_monday, INTERVAL 1 DAY), ' 07:00:00'), 30, 0, 1, 'SEM001', 'SUB003',
 (SELECT user_id FROM core_teacher WHERE teacherCode = 'IT001' LIMIT 1)),

('CC004', 'CS104-01', 'Web Development - Class 1', 'Room 104', 
 CONCAT(DATE_ADD(@base_monday, INTERVAL 1 DAY), ' 09:00:00'), 30, 0, 1, 'SEM001', 'SUB004',
 (SELECT user_id FROM core_teacher WHERE teacherCode = 'IT002' LIMIT 1)),

-- Wednesday classes (7:00-9:00, 13:00-15:00)
('CC005', 'CS201-01', 'Advanced Programming - Class 1', 'Room 201', 
 CONCAT(DATE_ADD(@base_monday, INTERVAL 2 DAY), ' 07:00:00'), 25, 0, 1, 'SEM001', 'SUB005',
 (SELECT user_id FROM core_teacher WHERE teacherCode = 'IT001' LIMIT 1)),

('CC006', 'CS202-01', 'Software Engineering - Class 1', 'Room 202', 
 CONCAT(DATE_ADD(@base_monday, INTERVAL 2 DAY), ' 13:00:00'), 25, 0, 1, 'SEM001', 'SUB006',
 (SELECT user_id FROM core_teacher WHERE teacherCode = 'IT002' LIMIT 1)),

-- Thursday classes (9:00-11:00, 13:00-15:00)
('CC007', 'BA101-01', 'Introduction to Business - Class 1', 'Room 301', 
 CONCAT(DATE_ADD(@base_monday, INTERVAL 3 DAY), ' 09:00:00'), 30, 0, 1, 'SEM001', 'SUB007',
 (SELECT user_id FROM core_teacher WHERE teacherCode = 'BUS001' LIMIT 1)),

('CC008', 'BA102-01', 'Business Management - Class 1', 'Room 302', 
 CONCAT(DATE_ADD(@base_monday, INTERVAL 3 DAY), ' 13:00:00'), 30, 0, 1, 'SEM001', 'SUB008',
 (SELECT user_id FROM core_teacher WHERE teacherCode = 'BUS001' LIMIT 1)),

-- Friday classes (7:00-9:00, 15:00-17:00)
('CC009', 'ENG101-01', 'Engineering Principles - Class 1', 'Room 401', 
 CONCAT(DATE_ADD(@base_monday, INTERVAL 4 DAY), ' 07:00:00'), 30, 0, 1, 'SEM001', 'SUB009',
 (SELECT user_id FROM core_teacher WHERE teacherCode = 'ENG001' LIMIT 1)),

('CC010', 'ENG102-01', 'Structural Analysis - Class 1', 'Room 402', 
 CONCAT(DATE_ADD(@base_monday, INTERVAL 4 DAY), ' 15:00:00'), 30, 0, 1, 'SEM001', 'SUB010',
 (SELECT user_id FROM core_teacher WHERE teacherCode = 'ENG001' LIMIT 1)),

-- Additional classes for variety (Monday afternoon, Tuesday evening)
('CC011', 'CS101-02', 'Programming Fundamentals - Class 2', 'Room 105', 
 CONCAT(@base_monday, ' 13:00:00'), 30, 0, 1, 'SEM001', 'SUB001',
 (SELECT user_id FROM core_teacher WHERE teacherCode = 'IT001' LIMIT 1)),

('CC012', 'CS102-02', 'Data Structures - Class 2', 'Room 106', 
 CONCAT(DATE_ADD(@base_monday, INTERVAL 1 DAY), ' 15:00:00'), 30, 0, 1, 'SEM001', 'SUB002',
 (SELECT user_id FROM core_teacher WHERE teacherCode = 'IT002' LIMIT 1)),

-- Saturday morning classes (optional)
('CC013', 'CS103-02', 'Database Systems - Class 2', 'Room 107', 
 CONCAT(DATE_ADD(@base_monday, INTERVAL 5 DAY), ' 07:00:00'), 30, 0, 1, 'SEM001', 'SUB003',
 (SELECT user_id FROM core_teacher WHERE teacherCode = 'IT001' LIMIT 1)),

('CC014', 'CS104-02', 'Web Development - Class 2', 'Room 108', 
 CONCAT(DATE_ADD(@base_monday, INTERVAL 5 DAY), ' 09:00:00'), 30, 0, 1, 'SEM001', 'SUB004',
 (SELECT user_id FROM core_teacher WHERE teacherCode = 'IT002' LIMIT 1));

-- Use INSERT IGNORE to avoid duplicates if courses already exist
-- If you want to update existing courses with schedule, use:
-- UPDATE `core_courseclass` SET `schedule` = ... WHERE `courseClassId` = 'CC001';

-- ============================================================================
-- Re-enable foreign key checks
-- ============================================================================

SET FOREIGN_KEY_CHECKS = 1;

-- ============================================================================
-- STEP 8: Update existing CourseClasses with schedule if they exist
-- ============================================================================

-- Update schedule for existing courses (if they were created without schedule)
UPDATE `core_courseclass` SET 
    `schedule` = CONCAT(@base_monday, ' 07:00:00'),
    `status` = 1
WHERE `courseClassId` = 'CC001' AND `schedule` IS NULL;

UPDATE `core_courseclass` SET 
    `schedule` = CONCAT(@base_monday, ' 09:00:00'),
    `status` = 1
WHERE `courseClassId` = 'CC002' AND `schedule` IS NULL;

UPDATE `core_courseclass` SET 
    `schedule` = CONCAT(DATE_ADD(@base_monday, INTERVAL 1 DAY), ' 07:00:00'),
    `status` = 1
WHERE `courseClassId` = 'CC003' AND `schedule` IS NULL;

UPDATE `core_courseclass` SET 
    `schedule` = CONCAT(DATE_ADD(@base_monday, INTERVAL 1 DAY), ' 09:00:00'),
    `status` = 1
WHERE `courseClassId` = 'CC004' AND `schedule` IS NULL;

-- ============================================================================
-- VERIFICATION QUERIES
-- ============================================================================

-- Check total students imported
SELECT COUNT(*) as total_students FROM core_student;

-- Check students by class
SELECT sc.className, COUNT(s.user_id) as student_count 
FROM core_studentclass sc 
LEFT JOIN core_student s ON sc.classId = s.studentClass_id 
GROUP BY sc.classId, sc.className;

-- Check students by department
SELECT d.departmentName, COUNT(s.user_id) as student_count
FROM core_department d
JOIN core_major m ON d.departmentId = m.department_id
JOIN core_studentclass sc ON m.majorId = sc.major_id
LEFT JOIN core_student s ON sc.classId = s.studentClass_id
GROUP BY d.departmentId, d.departmentName;

-- Check course classes with schedule
SELECT 
    cc.courseClassId,
    cc.courseCode,
    cc.courseName,
    cc.room,
    cc.schedule,
    DATE_FORMAT(cc.schedule, '%W %d/%m/%Y %H:%i') as formatted_schedule,
    s.subjectName,
    t.teacherCode,
    sem.semesterName
FROM core_courseclass cc
LEFT JOIN core_subject s ON cc.subject_id = s.subjectId
LEFT JOIN core_teacher t ON cc.teacher_id = t.user_id
LEFT JOIN core_semester sem ON cc.semester_id = sem.semesterId
WHERE cc.schedule IS NOT NULL
ORDER BY cc.schedule;

-- Check courses by day of week
SELECT 
    DAYNAME(cc.schedule) as day_of_week,
    DATE_FORMAT(cc.schedule, '%H:%i') as time_slot,
    COUNT(*) as course_count,
    GROUP_CONCAT(cc.courseCode ORDER BY cc.schedule SEPARATOR ', ') as courses
FROM core_courseclass cc
WHERE cc.schedule IS NOT NULL
GROUP BY DAYNAME(cc.schedule), DATE_FORMAT(cc.schedule, '%H:%i')
ORDER BY 
    FIELD(DAYNAME(cc.schedule), 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'),
    DATE_FORMAT(cc.schedule, '%H:%i');

-- ============================================================================
-- NOTES:
-- ============================================================================
-- 1. Password for all students: 'python123'
-- 2. All students have enrollmentYear = 2024
-- 3. All students start with gpa = 0.0 and totalCredits = 0
-- 4. Students are distributed across 5 classes (CL001-CL005)
-- 5. If users already exist, use INSERT IGNORE or adjust user_id values
-- 6. Make sure to adjust @next_user_id based on your existing user IDs
-- 7. Ensure teachers with IDs exist for advisorTeacher_id in StudentClass
-- 8. Course Schedule:
--    - Schedule is stored as DateTime (YYYY-MM-DD HH:MM:SS)
--    - Based on Monday of current week (@base_monday)
--    - Monday: 7:00, 9:00, 13:00
--    - Tuesday: 7:00, 9:00, 15:00
--    - Wednesday: 7:00, 13:00
--    - Thursday: 9:00, 13:00
--    - Friday: 7:00, 15:00
--    - Saturday: 7:00, 9:00 (optional)
-- 9. All schedules are calculated relative to current week's Monday
-- 10. Schedule format: 'YYYY-MM-DD HH:MM:SS' (e.g., '2024-10-28 07:00:00')
-- ============================================================================

