-- ============================================================================
-- SQL Script to Update Course Schedules
-- File: update_course_schedules.sql
-- Description: Update schedule for existing courses (especially CC001)
-- Usage: mysql -u username -p database_name < update_course_schedules.sql
-- ============================================================================

-- Calculate base date (Monday of current week)
SET @base_monday = DATE_SUB(CURDATE(), INTERVAL WEEKDAY(CURDATE()) DAY);

-- Update schedule for CC001 (Programming Fundamentals - Class 1)
-- Monday 7:00 AM
UPDATE `core_courseclass` 
SET `schedule` = CONCAT(@base_monday, ' 07:00:00')
WHERE `courseClassId` = 'CC001' AND (`schedule` IS NULL OR `schedule` = '');

-- Update schedule for CC002 (Data Structures - Class 1)
-- Monday 9:00 AM
UPDATE `core_courseclass` 
SET `schedule` = CONCAT(@base_monday, ' 09:00:00')
WHERE `courseClassId` = 'CC002' AND (`schedule` IS NULL OR `schedule` = '');

-- Update schedule for CC003 (Database Systems - Class 1)
-- Tuesday 7:00 AM
UPDATE `core_courseclass` 
SET `schedule` = CONCAT(DATE_ADD(@base_monday, INTERVAL 1 DAY), ' 07:00:00')
WHERE `courseClassId` = 'CC003' AND (`schedule` IS NULL OR `schedule` = '');

-- Update schedule for CC004 (Web Development - Class 1)
-- Tuesday 9:00 AM
UPDATE `core_courseclass` 
SET `schedule` = CONCAT(DATE_ADD(@base_monday, INTERVAL 1 DAY), ' 09:00:00')
WHERE `courseClassId` = 'CC004' AND (`schedule` IS NULL OR `schedule` = '');

-- Verify updates
SELECT 
    cc.courseClassId,
    cc.courseCode,
    cc.courseName,
    cc.schedule,
    DATE_FORMAT(cc.schedule, '%W %d/%m/%Y %H:%i') as formatted_schedule,
    DAYNAME(cc.schedule) as day_of_week,
    TIME(cc.schedule) as time_slot
FROM core_courseclass cc
WHERE cc.courseClassId IN ('CC001', 'CC002', 'CC003', 'CC004')
ORDER BY cc.schedule;

-- ============================================================================
-- NOTES:
-- ============================================================================
-- 1. This script updates schedules for courses that don't have one
-- 2. Schedules are based on Monday of current week
-- 3. Each class is 2 hours long (can be adjusted)
-- 4. After running, refresh the frontend to see updated schedules
-- ============================================================================

