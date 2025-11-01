"""
Script để tạo course class mới với lịch học vào thứ 3 (Tuesday)
Chạy: python create_tuesday_course.py
"""

import os
import sys
import django

# Fix encoding for Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_management.settings')
django.setup()

from core.models import CourseClass, Subject, Semester, Teacher, Department
from datetime import datetime, timedelta, time as time_class
from django.utils import timezone

print("=" * 60)
print("Creating Course Class with Tuesday Schedule")
print("=" * 60)

# Calculate Tuesday of current week
today = datetime.now().date()
days_since_monday = today.weekday()  # 0=Monday, 6=Sunday
monday_this_week = today - timedelta(days=days_since_monday)
tuesday_this_week = monday_this_week + timedelta(days=1)

print(f"Base Monday: {monday_this_week}")
print(f"Tuesday: {tuesday_this_week}")

# Get or create required data
print("\n[Step 1] Getting/Creating required data...")

# Get Department
try:
    dept = Department.objects.get(departmentCode='IT')
    print(f"  [OK] Department: {dept.departmentName}")
except Department.DoesNotExist:
    print("  [ERROR] Department IT not found. Please run import_students.sql first.")
    sys.exit(1)

# Get or create Subject
subject_code = 'CS105'
subject_name = 'Computer Networks'
subject, created = Subject.objects.get_or_create(
    subjectCode=subject_code,
    defaults={
        'subjectId': f'SUB{subject_code.replace("CS", "")}',
        'subjectName': subject_name,
        'credits': 3,
        'theoryHours': 30,
        'practiceHours': 30,
        'status': 'active',
        'department': dept
    }
)
if created:
    print(f"  [OK] Created subject: {subject_name} ({subject_code})")
else:
    print(f"  [OK] Found subject: {subject_name} ({subject_code})")

# Get or create Semester
semester, created = Semester.objects.get_or_create(
    semesterId='SEM001',
    defaults={
        'semesterCode': '2024-1',
        'semesterName': 'Semester 1 - 2024',
        'startDate': datetime(2024, 9, 1).date(),
        'endDate': datetime(2024, 12, 31).date(),
        'registrationStart': timezone.now() - timedelta(days=7),
        'registrationEnd': timezone.now() + timedelta(days=30),
        'status': 'active'
    }
)
if created:
    print(f"  [OK] Created semester: {semester.semesterName}")
else:
    print(f"  [OK] Found semester: {semester.semesterName}")

# Get Teacher
try:
    teacher = Teacher.objects.get(teacherCode='IT001')
    print(f"  [OK] Teacher: {teacher.user.full_name}")
except Teacher.DoesNotExist:
    print("  [ERROR] Teacher IT001 not found. Please run import_students.sql first.")
    sys.exit(1)

# Create schedule for Tuesday
print("\n[Step 2] Creating course class with Tuesday schedule...")

# Options for Tuesday schedule times
tuesday_times = [
    (9, 0, '09:00-11:00'),   # Morning
    (13, 0, '13:00-15:00'),  # Afternoon
    (15, 0, '15:00-17:00'),  # Evening
]

print("Available time slots for Tuesday:")
for idx, (hour, minute, time_str) in enumerate(tuesday_times, 1):
    print(f"  {idx}. {time_str}")

# Use first time slot (can be modified)
selected_hour, selected_minute, time_str = tuesday_times[0]
schedule_datetime = timezone.make_aware(
    datetime.combine(tuesday_this_week, time_class(hour=selected_hour, minute=selected_minute))
)

# Generate course class ID
existing_courses = CourseClass.objects.filter(courseCode__startswith=f'{subject_code}-').count()
course_class_id = f'CC{100 + existing_courses + 1:03d}'
course_code = f'{subject_code}-{existing_courses + 1:02d}'

# Create CourseClass
course_class, created = CourseClass.objects.get_or_create(
    courseClassId=course_class_id,
    defaults={
        'courseCode': course_code,
        'courseName': f'{subject_name} - Class {existing_courses + 1}',
        'subject': subject,
        'teacher': teacher,
        'semester': semester,
        'room': 'Room 201',
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
    print(f"\n  [INFO] Course class {course_class_id} already exists:")
    print(f"    - Schedule: {course_class.schedule.strftime('%A %Y-%m-%d %H:%M') if course_class.schedule else 'None'}")
    # Update schedule if it's NULL
    if not course_class.schedule:
        course_class.schedule = schedule_datetime
        course_class.save()
        print(f"    - [UPDATED] Schedule set to: {schedule_datetime.strftime('%A %Y-%m-%d %H:%M')}")

print("\n" + "=" * 60)
print("[SUCCESS] Course class created/updated with Tuesday schedule!")
print("=" * 60)

