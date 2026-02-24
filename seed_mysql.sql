-- Sample seed data for MySQL
-- Assumes Django migrations already created tables.

CREATE DATABASE IF NOT EXISTS course_registration
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE course_registration;

SET FOREIGN_KEY_CHECKS = 0;

-- Clear existing data
TRUNCATE TABLE courses_registration;
TRUNCATE TABLE courses_course;
TRUNCATE TABLE accounts_user;
TRUNCATE TABLE courses_registrationwindow;

-- Sample users (passwords: Password123! and Admin123!)
INSERT INTO accounts_user (
  id, password, last_login, is_superuser, username, first_name, last_name,
  email, is_staff, is_active, date_joined, mssv
) VALUES
  (1, 'pbkdf2_sha256$870000$jqylm1CA0GlbfeJCefcOoG$FPWqO+6vLsQcE+BcauINzFSoMiDbcVjWPF7KpaptaHY=', NULL, 0, 'sv001', 'An', 'Nguyen', 'phamquyet472k4@gmail.com', 0, 1, '2026-02-24 00:00:00', '20123456'),
  (2, 'pbkdf2_sha256$870000$9KzroofR7Ie1fCS32t07f5$odEy1ettJarFKSIRX0sUzWRFj2Iurb70bCRoRYO3uWw=', NULL, 1, 'admin', 'Admin', 'User', 'enormitpham@gmail.com', 1, 1, '2026-02-24 00:00:00', '00000000');

-- Sample courses
INSERT INTO courses_course (id, code, name, credits) VALUES
  (1, 'MATH101', 'Giai tich 1', 3),
  (2, 'PHYS101', 'Vat ly dai cuong', 3),
  (3, 'CS101', 'Nhap mon lap trinh', 4),
  (4, 'CS102', 'Cau truc du lieu', 4),
  (5, 'ENG101', 'Tieng Anh 1', 2);

-- Registration window (id=1)
INSERT INTO courses_registrationwindow (id, is_open, start_at, end_at, updated_at) VALUES
  (1, 1, NULL, NULL, '2026-02-24 00:00:00');

SET FOREIGN_KEY_CHECKS = 1;
