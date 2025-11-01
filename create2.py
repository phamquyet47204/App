"""
Script tạo dữ liệu mẫu bổ sung cho University Management System
Bổ sung thêm dữ liệu để test các tính năng
"""

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_management.settings')
django.setup()

from core.models import *
from django.contrib.auth.hashers import make_password
from datetime import datetime, date, timedelta
from decimal import Decimal
import random

print("=" * 60)
print("🚀 Creating Additional Sample Data")
print("=" * 60)

# ============================================================================
# 1. TẠO THÊM STUDENTS (nếu chưa có)
# ============================================================================
print("\n👨‍🎓 Step 1: Creating Additional Students...")
students_to_create = []
for i in range(21, 51):  # Students 21-50
    username = f'student{i}'
    try:
        user = User.objects.get(username=username)
        student = Student.objects.get(user=user)
    except (User.DoesNotExist, Student.DoesNotExist):
        user = User.objects.create(
            username=username,
            email=f'{username}@test.com',
            user_type='student',
            full_name=f'Student {i}',
            phone=f'032{i:07d}',
            password=make_password('python123'),
            status='active'
        )
        
        # Get random class
        classes = list(StudentClass.objects.all()[:4])
        if classes:
            student_class = random.choice(classes)
            student = Student.objects.create(
                studentId=f'S{i:03d}',
                user=user,
                studentCode=f'SE{i:03d}',
                studentClass=student_class,
                dateOfBirth=date(2000, 1, 1),
                gender=random.choice(['male', 'female']),
                enrollmentYear=2024,
                gpa=Decimal('0.0'),
                totalCredits=0
            )
            # Update currentStudents
            student_class.currentStudents += 1
            student_class.save()
            students_to_create.append(student)
            print(f"  ✓ Created: {student.studentCode}")

print(f"  ✓ Created/Found {len(students_to_create)} additional students")

# ============================================================================
# 2. TẠO THÊM COURSE REGISTRATIONS
# ============================================================================
print("\n📋 Step 2: Creating Additional Course Registrations...")
all_students = list(Student.objects.all()[:50])
all_courses = list(CourseClass.objects.filter(status=True)[:7])
semester = Semester.objects.filter(status='active').first()

if semester and all_courses:
    reg_count = 0
    for student in all_students[15:]:  # Students 16-50
        # Register 1-3 courses
        random_courses = random.sample(all_courses, random.randint(1, 3))
        for j, course_class in enumerate(random_courses):
            reg, created = CourseRegistration.objects.get_or_create(
                registrationId=f'REG{student.studentId}{j:03d}',
                defaults={
                    'student': student,
                    'courseClass': course_class,
                    'semester': semester,
                    'registrationDate': date(2024, 8, random.randint(15, 30)),
                    'status': 'registered'
                }
            )
            if created:
                reg_count += 1
                # Update currentStudents
                course_class.currentStudents += 1
                course_class.save()
    
    print(f"  ✓ Created {reg_count} additional registrations")

# ============================================================================
# 3. TẠO THÊM GRADES
# ============================================================================
print("\n📊 Step 3: Creating Additional Grades...")
def calculate_grade_from_score(average_score):
    """Tính letterGrade và gradePoint từ average_score (thang điểm 10)"""
    if average_score is None:
        return None, None, None
    score = float(average_score)
    if score >= 9.0:
        return 'A', 4.0, True
    elif score >= 8.5:
        return 'B+', 3.5, True
    elif score >= 8.0:
        return 'B', 3.0, True
    elif score >= 7.5:
        return 'C+', 2.5, True
    elif score >= 7.0:
        return 'C', 2.0, True
    elif score >= 6.5:
        return 'D+', 1.5, True
    elif score >= 6.0:
        return 'D', 1.0, True
    else:
        return 'F', 0.0, False

grade_count = 0

for student in all_students[10:20]:  # Students 11-20
    registrations = CourseRegistration.objects.filter(
        student=student,
        semester=semester,
        status='registered'
    )[:3]
    
    for j, reg in enumerate(registrations):
        course_class = reg.courseClass
        subject = course_class.subject
        
        # Generate random scores
        avg_score = Decimal(str(round(random.uniform(6.5, 9.5), 1)))
        
        # Tự động tính letterGrade và gradePoint từ average_score
        letter_grade, grade_point, is_passed = calculate_grade_from_score(avg_score)
        
        grade, created = Grade.objects.get_or_create(
            gradeId=f'GR{student.studentId}{j+1:02d}',
            defaults={
                'student': student,
                'subject': subject,
                'teacher': course_class.teacher,
                'courseClass': course_class,
                'semester': semester,
                'assginmentscore': Decimal(str(round(random.uniform(7.0, 10.0), 1))),
                'midterm_score': Decimal(str(round(random.uniform(6.0, 9.5), 1))),
                'final_score': Decimal(str(round(random.uniform(6.5, 9.8), 1))),
                'average_score': avg_score,
                'letterGrade': letter_grade,
                'gradePoint': Decimal(str(grade_point)),
                'isPassed': is_passed
            }
        )
        if created:
            grade_count += 1

print(f"  ✓ Created {grade_count} additional grades")

# ============================================================================
# 4. TẠO THÊM DOCUMENT REQUESTS
# ============================================================================
print("\n📝 Step 4: Creating Additional Document Requests...")
doc_types = list(DocumentType.objects.filter(status='active'))
request_statuses = ['pending', 'approved', 'completed']
doc_request_count = 0

if semester and doc_types:
    for i, student in enumerate(all_students[10:25]):  # Students 11-25
        doc_type = random.choice(doc_types)
        
        # Check if already exists
        existing = DocumentRequest.objects.filter(
            student=student,
            documentType=doc_type,
            semester=semester,
            status__in=['pending', 'approved', 'completed']
        ).first()
        
        if not existing:
            status = random.choice(request_statuses)
            request_date = date.today() - timedelta(days=random.randint(1, 30))
            
            doc_request = DocumentRequest.objects.create(
                requestId=f'DR{len(DocumentRequest.objects.all()) + i + 1:06d}',
                student=student,
                documentType=doc_type,
                semester=semester,
                requestDate=datetime.combine(request_date, datetime.min.time()),
                purpose=f'Request for {doc_type.name.lower()}',
                status=status
            )
            doc_request_count += 1

print(f"  ✓ Created {doc_request_count} additional document requests")

# ============================================================================
# 5. TẠO THÊM NOTIFICATION RECIPIENTS
# ============================================================================
print("\n🔔 Step 5: Creating Additional Notification Recipients...")
notifications = Notification.objects.all()[:5]
recipient_count = 0

for notification in notifications:
    for student in all_students[15:35]:  # Students 16-35
        recipient, created = NotificationRecipient.objects.get_or_create(
            recipientId=f'{notification.notificationId}_{student.user.username}',
            defaults={
                'notification': notification,
                'user': student.user,
                'deliveryStatus': 'delivered',
                'deliveredAt': datetime.now() - timedelta(days=random.randint(0, 7))
            }
        )
        if created:
            recipient_count += 1

print(f"  ✓ Created {recipient_count} additional notification recipients")

# ============================================================================
# 6. TẠO THÊM TUITION FEES
# ============================================================================
print("\n💰 Step 6: Creating Additional Tuition Fees...")
payment_statuses = ['unpaid', 'partial_paid', 'paid']
tuition_count = 0

if semester:
    for student in all_students[15:30]:  # Students 16-30
        # Check if already exists
        existing = TuitionFee.objects.filter(
            student=student,
            semester=semester
        ).exists()
        
        if not existing:
            payment_status = random.choice(payment_statuses)
            total_credit = random.randint(12, 18)
            fee_per_credit = Decimal('500000')
            total_amount = Decimal(str(total_credit * 500000))
            
            if payment_status == 'unpaid':
                paid_amount = Decimal('0')
            elif payment_status == 'partial_paid':
                paid_amount = total_amount / 2
            else:
                paid_amount = total_amount
            
            tuition = TuitionFee.objects.create(
                tuitionFee=f'TF{student.studentId}',
                student=student,
                semester=semester,
                totalCredit=total_credit,
                feePerCredit=fee_per_credit,
                totalAmount=total_amount,
                paidAmount=paid_amount,
                paymentStatus=payment_status,
                dueDate=date.today() + timedelta(days=30)
            )
            tuition_count += 1

print(f"  ✓ Created {tuition_count} additional tuition fees")

# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "=" * 60)
print("✅ Additional Sample Data Creation Completed!")
print("=" * 60)
print(f"\n📊 Updated Summary:")
print(f"  - Students: {Student.objects.count()}")
print(f"  - Registrations: {CourseRegistration.objects.count()}")
print(f"  - Grades: {Grade.objects.count()}")
print(f"  - Document Requests: {DocumentRequest.objects.count()}")
print(f"  - Notification Recipients: {NotificationRecipient.objects.count()}")
print(f"  - Tuition Fees: {TuitionFee.objects.count()}")

print("\n" + "=" * 60)
