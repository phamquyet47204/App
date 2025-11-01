"""
Script để update schedule cho courses
Chạy: python update_schedules.py
"""

import os
import sys
import django

# Fix encoding for Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_management.settings')
django.setup()

from core.models import CourseClass
from datetime import datetime, timedelta, time as time_class
from django.utils import timezone

print("=" * 60)
print("Updating Course Schedules")
print("=" * 60)

# Calculate base date (Monday of current week)
today = datetime.now().date()
days_since_monday = today.weekday()  # 0=Monday, 6=Sunday
monday_this_week = today - timedelta(days=days_since_monday)

print(f"Base Monday: {monday_this_week}")

# Update schedules
schedules = {
    'CC001': (monday_this_week, 7, 0),   # Monday 7:00
    'CC002': (monday_this_week, 9, 0),   # Monday 9:00
    'CC003': (monday_this_week + timedelta(days=1), 7, 0),   # Tuesday 7:00
    'CC004': (monday_this_week + timedelta(days=1), 9, 0),   # Tuesday 9:00
    'CC005': (monday_this_week + timedelta(days=2), 7, 0),   # Wednesday 7:00
    'CC006': (monday_this_week + timedelta(days=2), 13, 0),  # Wednesday 13:00
    'CC007': (monday_this_week + timedelta(days=3), 9, 0),   # Thursday 9:00
    'CC008': (monday_this_week + timedelta(days=3), 13, 0),  # Thursday 13:00
    'CC009': (monday_this_week + timedelta(days=4), 7, 0),   # Friday 7:00
    'CC010': (monday_this_week + timedelta(days=4), 15, 0),  # Friday 15:00
    'CC011': (monday_this_week, 13, 0),  # Monday 13:00
    'CC012': (monday_this_week + timedelta(days=1), 15, 0), # Tuesday 15:00
    'CC013': (monday_this_week + timedelta(days=5), 7, 0),  # Saturday 7:00
    'CC014': (monday_this_week + timedelta(days=5), 9, 0),  # Saturday 9:00
}

updated_count = 0
for course_id, (date, hour, minute) in schedules.items():
    try:
        course = CourseClass.objects.get(courseClassId=course_id)
        if not course.schedule:  # Only update if schedule is NULL
            # Create timezone-aware datetime
            schedule_datetime = timezone.make_aware(
                datetime.combine(date, time_class(hour=hour, minute=minute))
            )
            course.schedule = schedule_datetime
            course.save()
            print(f"  [OK] Updated {course_id}: {course.courseCode} - {schedule_datetime.strftime('%A %Y-%m-%d %H:%M')}")
            updated_count += 1
        else:
            print(f"  [SKIP] {course_id}: Already has schedule - {course.schedule.strftime('%A %Y-%m-%d %H:%M')}")
    except CourseClass.DoesNotExist:
        print(f"  [ERROR] Course {course_id} not found")

print(f"\n[SUCCESS] Updated {updated_count} courses")
print("=" * 60)

