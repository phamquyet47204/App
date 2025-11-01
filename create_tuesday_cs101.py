"""
Script để tạo thêm class của CS101 (Programming Fundamentals) với lịch học vào thứ 3
Chạy: python create_tuesday_cs101.py
"""

import os
import sys
import django

# Fix encoding for Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_management.settings')
django.setup()

from core.models import CourseClass, Subject, Semester, Teacher
from datetime import datetime, timedelta, time as time_class
from django.utils import timezone

print("=" * 60)
print("Creating CS101 Class with Tuesday Schedule")
print("=" * 60)

# Calculate Tuesday of current week
today = datetime.now().date()
days_since_monday = today.weekday()  # 0=Monday, 6=Sunday
monday_this_week = today - timedelta(days=days_since_monday)
tuesday_this_week = monday_this_week + timedelta(days=1)

print(f"Base Monday: {monday_this_week}")
print(f"Tuesday: {tuesday_this_week}")

# Get required data
print("\n[Step 1] Getting required data...")

try:
    subject = Subject.objects.get(subjectCode='CS101')
    print(f"  [OK] Subject: {subject.subjectName}")
except Subject.DoesNotExist:
    print("  [ERROR] Subject CS101 not found. Please run import_students.sql first.")
    sys.exit(1)

try:
    semester = Semester.objects.get(semesterId='SEM001')
    print(f"  [OK] Semester: {semester.semesterName}")
except Semester.DoesNotExist:
    print("  [ERROR] Semester SEM001 not found. Please run import_students.sql first.")
    sys.exit(1)

try:
    teacher = Teacher.objects.get(teacherCode='IT001')
    print(f"  [OK] Teacher: {teacher.user.full_name}")
except Teacher.DoesNotExist:
    print("  [ERROR] Teacher IT001 not found. Please run import_students.sql first.")
    sys.exit(1)

# Check existing CS101 classes
existing_classes = CourseClass.objects.filter(
    subject=subject,
    semester=semester
).order_by('courseCode')

print(f"\n[Step 2] Found {existing_classes.count()} existing CS101 classes:")
for cls in existing_classes:
    schedule_info = cls.schedule.strftime('%A %H:%M') if cls.schedule else 'No schedule'
    print(f"  - {cls.courseCode}: {schedule_info}")

# Determine next class number
if existing_classes.exists():
    last_class = existing_classes.last()
    # Extract number from courseCode (e.g., CS101-01 -> 01)
    try:
        last_num = int(last_class.courseCode.split('-')[1])
        next_num = last_num + 1
    except (ValueError, IndexError):
        next_num = existing_classes.count() + 1
else:
    next_num = 1

course_code = f'CS101-{next_num:02d}'

# Generate course class ID - find next available
course_class_num = 100
while True:
    course_class_id = f'CC{course_class_num:03d}'
    if not CourseClass.objects.filter(courseClassId=course_class_id).exists():
        break
    course_class_num += 1

# Create schedule for Tuesday - multiple time options
tuesday_times = [
    (9, 0, '09:00-11:00'),   # Morning
    (13, 0, '13:00-15:00'),  # Afternoon
    (15, 0, '15:00-17:00'),  # Evening
]

# Check which times are already taken on Tuesday
taken_times = []
for cls in existing_classes:
    if cls.schedule:
        schedule_day = cls.schedule.weekday()  # 0=Monday, 1=Tuesday
        if schedule_day == 1:  # Tuesday
            schedule_time = cls.schedule.time()
            taken_times.append((schedule_time.hour, schedule_time.minute))

# Find available time slot
available_time = None
for hour, minute, time_str in tuesday_times:
    if (hour, minute) not in taken_times:
        available_time = (hour, minute, time_str)
        break

if not available_time:
    # If all slots taken, use first one anyway (multiple classes can be at same time)
    available_time = tuesday_times[0]

selected_hour, selected_minute, time_str = available_time
schedule_datetime = timezone.make_aware(
    datetime.combine(tuesday_this_week, time_class(hour=selected_hour, minute=selected_minute))
)

print(f"\n[Step 3] Creating new class with Tuesday schedule...")
print(f"  - Time slot: {time_str}")

# Create CourseClass
course_class, created = CourseClass.objects.get_or_create(
    courseClassId=course_class_id,
    defaults={
        'courseCode': course_code,
        'courseName': f'Programming Fundamentals - Class {next_num}',
        'subject': subject,
        'teacher': teacher,
        'semester': semester,
        'room': f'Room {100 + next_num}',  # Room 101, 102, etc.
        'schedule': schedule_datetime,
        'maxStudents': 30,
        'currentStudents': 0,
        'status': True
    }
)

if created:
    print(f"\n  [SUCCESS] Created course class:")
    print(f"    - Course ID: {course_class_id}")
    print(f"    - Course Code: {course_code}")
    print(f"    - Course Name: {course_class.courseName}")
    print(f"    - Schedule: {schedule_datetime.strftime('%A %Y-%m-%d %H:%M')} ({time_str})")
    print(f"    - Room: {course_class.room}")
    print(f"    - Teacher: {teacher.user.full_name}")
    print(f"    - Max Students: {course_class.maxStudents}")
else:
    print(f"\n  [INFO] Course class {course_class_id} already exists")
    if not course_class.schedule:
        course_class.schedule = schedule_datetime
        course_class.save()
        print(f"    - [UPDATED] Schedule set to: {schedule_datetime.strftime('%A %Y-%m-%d %H:%M')}")

print("\n" + "=" * 60)
print("[SUCCESS] New CS101 class created with Tuesday schedule!")
print("=" * 60)
print("\nAll CS101 classes now:")
all_cs101 = CourseClass.objects.filter(subject=subject, semester=semester).order_by('courseCode')
for cls in all_cs101:
    schedule_info = cls.schedule.strftime('%A %H:%M') if cls.schedule else 'No schedule'
    print(f"  - {cls.courseCode} ({cls.courseClassId}): {schedule_info}")

