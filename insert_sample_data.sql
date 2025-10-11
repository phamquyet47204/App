-- Insert Sample Data for Student Management System
USE university_db;

SET FOREIGN_KEY_CHECKS = 1;

-- 1. Insert Users (Password: python123 for all)
INSERT INTO core_user (id, username, password, email, full_name, phone, user_type, status, is_superuser, is_staff, is_active, first_name, last_name, date_joined, created_at, updated_at) VALUES
(1, 'admin', 'pbkdf2_sha256$600000$D6YCRzIBv4L7HlJfWvxz9a$33CGpWzer5yz2pl9eREe2MbmDoK5SObedt5QnibPN2M=', 'admin@test.com', 'Admin User', '0901234567', 'admin', 'active', 1, 1, 1, 'Admin', 'User', NOW(), NOW(), NOW()),
(2, 'teacher1', 'pbkdf2_sha256$600000$u1OumppQOAQtMX009EOc0Y$/3WXwquHiAz/XVSCt+NdCj38cSC8C97aLjHoDitqR9Y=', 'teacher1@test.com', 'Nguyen Van A', '0902345678', 'teacher', 'active', 0, 0, 1, 'Van A', 'Nguyen', NOW(), NOW(), NOW()),
(3, 'teacher2', 'pbkdf2_sha256$600000$yMXzLLz3O0tqgbbx06IKVX$d7W/NlMpKW03bIOsIuER1RkFIJXD4PojznhB0qIOJG8=', 'teacher2@test.com', 'Tran Thi B', '0903456789', 'teacher', 'active', 0, 0, 1, 'Thi B', 'Tran', NOW(), NOW(), NOW()),
(4, 'student1', 'pbkdf2_sha256$600000$SmFfO0EHmJoiTEvnN74GPt$s1H596+xtpPPIoCgyj3Qky8equ0W5cfNSn8lQsIbto0=', 'student1@test.com', 'Le Van C', '0904567890', 'student', 'active', 0, 0, 1, 'Van C', 'Le', NOW(), NOW(), NOW()),
(5, 'student2', 'pbkdf2_sha256$600000$VzgHNCwhu9FJKqjRlYn9U9$pL2rBaW3n1XHRpE7rhjLbWWSY4U1JlE6fJgiVee2ji0=', 'student2@test.com', 'Pham Thi D', '0905678901', 'student', 'active', 0, 0, 1, 'Thi D', 'Pham', NOW(), NOW(), NOW()),
(6, 'student3', 'pbkdf2_sha256$600000$j7WUDr4ChFtSB8Rq643GWZ$x7UWNvpTR2Hgr4vMN8PASTGu2nfnkxFeqLpbmw/2Uw8=', 'student3@test.com', 'Hoang Van E', '0906789012', 'student', 'active', 0, 0, 1, 'Van E', 'Hoang', NOW(), NOW(), NOW());

-- 2. Insert Departments
INSERT INTO core_department (departmentId, departmentCode, departmentName, headTeacher_id, status, createdAt) VALUES
('DEPT001', 'IT', 'Information Technology', NULL, 'active', NOW()),
('DEPT002', 'BUS', 'Business Administration', NULL, 'active', NOW()),
('DEPT003', 'ENG', 'Engineering', NULL, 'active', NOW());

-- 3. Insert Teachers
INSERT INTO core_teacher (user_id, teacherId, teacherCode, department_id, position, hireDate) VALUES
(2, 'TCH001', 'GV001', 'DEPT001', 'Lecturer', '2020-01-15'),
(3, 'TCH002', 'GV002', 'DEPT002', 'Senior Lecturer', '2019-03-20');

-- 4. Insert Majors
INSERT INTO core_major (majorId, majorCode, majorName, department_id, durationYears, totalCredits, status) VALUES
('MAJ001', 'CS', 'Computer Science', 'DEPT001', 4, 140, 1),
('MAJ002', 'BA', 'Business Administration', 'DEPT002', 4, 130, 1),
('MAJ003', 'SE', 'Software Engineering', 'DEPT001', 4, 145, 1);

-- 5. Insert Student Classes
INSERT INTO core_studentclass (classId, classCode, className, major_id, academicYear, advisorTeacher_id, maxStudents, currentStudents, status) VALUES
('CLS001', 'CS2021A', 'Computer Science 2021 A', 'MAJ001', '2021-2025', 2, 40, 2, 1),
('CLS002', 'BA2021A', 'Business Admin 2021 A', 'MAJ002', '2021-2025', 3, 35, 1, 1),
('CLS003', 'SE2022A', 'Software Engineering 2022 A', 'MAJ003', '2022-2026', 2, 40, 0, 1);

-- 6. Insert Students
INSERT INTO core_student (user_id, studentId, studentCode, studentClass_id, dateOfBirth, gender, enrollmentYear, gpa, totalCredits) VALUES
(4, 'STD001', 'SV001', 'CLS001', '2003-05-15', 'male', 2021, 3.5, 60),
(5, 'STD002', 'SV002', 'CLS001', '2003-08-20', 'female', 2021, 3.8, 65),
(6, 'STD003', 'SV003', 'CLS002', '2003-03-10', 'male', 2021, 3.2, 55);

-- 7. Insert Admin
INSERT INTO core_admin (user_id, adminId, adminCode) VALUES
(1, 'ADM001', 'AD001');

-- 8. Insert Academic Years
INSERT INTO core_academicyear (yearId, yearCode, yearName, startDate, endDate, status) VALUES
('AY2023', '2023-2024', 'Academic Year 2023-2024', '2023-09-01', '2024-06-30', 'active'),
('AY2024', '2024-2025', 'Academic Year 2024-2025', '2024-09-01', '2025-06-30', 'active');

-- 9. Insert Semesters
INSERT INTO core_semester (semesterId, semesterCode, semesterName, academicYear_id, startDate, endDate, registrationStart, registrationEnd, status) VALUES
('SEM001', '2023-1', 'Semester 1 - 2023', 'AY2023', '2023-09-01', '2024-01-15', '2023-08-01 00:00:00', '2023-08-31 23:59:59', 'active'),
('SEM002', '2023-2', 'Semester 2 - 2023', 'AY2023', '2024-02-01', '2024-06-30', '2024-01-01 00:00:00', '2024-01-31 23:59:59', 'active'),
('SEM003', '2024-1', 'Semester 1 - 2024', 'AY2024', '2024-09-01', '2025-01-15', '2024-08-01 00:00:00', '2024-08-31 23:59:59', 'active');

-- 10. Insert Subjects
INSERT INTO core_subject (subjectId, subjectCode, subjectName, department_id, credits, theoryHours, practiceHours, status) VALUES
('SUB001', 'CS101', 'Introduction to Programming', 'DEPT001', 3, 30, 30, 'active'),
('SUB002', 'CS102', 'Data Structures', 'DEPT001', 4, 45, 30, 'active'),
('SUB003', 'BUS101', 'Principles of Management', 'DEPT002', 3, 45, 0, 'active'),
('SUB004', 'CS201', 'Database Systems', 'DEPT001', 4, 40, 30, 'active'),
('SUB005', 'CS301', 'Web Development', 'DEPT001', 3, 30, 30, 'active');

-- 11. Insert Subject Prerequisites
INSERT INTO core_subject_prerequisites (from_subject_id, to_subject_id) VALUES
('SUB001', 'SUB002'),
('SUB002', 'SUB004');

-- 12. Insert Course Classes
INSERT INTO core_courseclass (courseClassId, courseCode, courseName, subject_id, teacher_id, semester_id, room, schedule, maxStudents, currentStudents, status) VALUES
('CC001', 'CS101-01', 'Intro Programming - Class 01', 'SUB001', 2, 'SEM001', 'A101', '2023-09-05 08:00:00', 40, 2, 1),
('CC002', 'CS102-01', 'Data Structures - Class 01', 'SUB002', 2, 'SEM001', 'A102', '2023-09-05 10:00:00', 35, 1, 1),
('CC003', 'BUS101-01', 'Management - Class 01', 'SUB003', 3, 'SEM001', 'B201', '2023-09-06 08:00:00', 40, 1, 1);

-- 13. Insert Course Registrations
INSERT INTO core_courseregistration (registrationId, student_id, courseClass_id, semester_id, registrationDate, status) VALUES
('REG001', 4, 'CC001', 'SEM001', '2023-08-15', 'completed'),
('REG002', 5, 'CC001', 'SEM001', '2023-08-16', 'completed'),
('REG003', 4, 'CC002', 'SEM001', '2023-08-15', 'registered'),
('REG004', 6, 'CC003', 'SEM001', '2023-08-17', 'completed');

-- 14. Insert Grades
INSERT INTO core_grade (gradeId, student_id, subject_id, teacher_id, courseClass_id, semester_id, assginmentscore, midterm_score, final_score, average_score, letterGrade, gradePoint, isPassed, createdAt, updatedAt) VALUES
('GRD001', 4, 'SUB001', 2, 'CC001', 'SEM001', 8.5, 8.0, 8.5, 8.3, 'A', 4.0, 1, NOW(), NOW()),
('GRD002', 5, 'SUB001', 2, 'CC001', 'SEM001', 9.0, 9.5, 9.0, 9.2, 'A+', 4.0, 1, NOW(), NOW()),
('GRD003', 6, 'SUB003', 3, 'CC003', 'SEM001', 7.0, 7.5, 7.0, 7.2, 'B', 3.0, 1, NOW(), NOW());

-- 15. Insert Document Types
INSERT INTO core_documenttype (documentTypeId, name, code, description, maxRequestsPerSemester, processingDays, status) VALUES
('DOC001', 'Student Certificate', 'CERT', 'Certificate of student status', 3, 3, 'active'),
('DOC002', 'Transcript', 'TRANS', 'Academic transcript', 5, 5, 'active'),
('DOC003', 'Recommendation Letter', 'RECOM', 'Letter of recommendation', 2, 7, 'active');

-- 16. Insert Tuition Fees
INSERT INTO core_tuitionfee (tuitionFee, student_id, semester_id, totalCredit, feePerCredit, totalAmount, paidAmount, paymentStatus, dueDate, paymentDate, updatedBy_id, notes) VALUES
('TUI001', 4, 'SEM001', 7, 500000, 3500000, 3500000, 'paid', '2023-09-30', '2023-09-15 10:00:00', 1, 'Paid in full'),
('TUI002', 5, 'SEM001', 3, 500000, 1500000, 1500000, 'paid', '2023-09-30', '2023-09-20 14:30:00', 1, 'Paid in full'),
('TUI003', 6, 'SEM001', 3, 500000, 1500000, 750000, 'partial_paid', '2023-09-30', NULL, 1, 'Partial payment received');

-- 17. Insert Notifications
INSERT INTO core_notification (notificationId, createdBy_id, title, content, targetAudience, targetId, notificationType, priority, scheduledAt, status) VALUES
('NOT001', 1, 'Welcome New Students', 'Welcome to the new academic year 2023-2024!', 'student', '[]', 'general', 1, '2023-09-01 08:00:00', 'active'),
('NOT002', 1, 'Exam Schedule Released', 'Final exam schedule for Semester 1 is now available.', 'all', '[]', 'academic', 2, '2023-12-01 09:00:00', 'active'),
('NOT003', 1, 'Tuition Fee Reminder', 'Please pay your tuition fees before the deadline.', 'student', '[]', 'administrative', 3, '2023-09-20 08:00:00', 'active');

SELECT 'Sample data inserted successfully!' AS message;
