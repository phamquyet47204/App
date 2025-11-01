"""
Script tạo dữ liệu mẫu cho University Management System
Sử dụng models từ core app với schema hiện tại
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
print("🚀 Creating Sample Data for University Management System")
print("=" * 60)

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_or_create_master_user():
    """Tạo hoặc lấy master admin user cho notifications"""
    master_user, created = User.objects.get_or_create(
        username='master',
        defaults={
            'email': 'master@admin.com',
            'user_type': 'admin',
            'full_name': 'Master Administrator',
            'password': make_password('master123'),
            'status': 'active',
            'is_staff': True,
            'is_superuser': True
        }
    )
    if created:
        print(f"  ✓ Created master user: {master_user.username}")
    return master_user

# ============================================================================
# 1. DEPARTMENTS
# ============================================================================
print("\n📁 Step 1: Creating Departments...")
departments_data = [
    {'departmentId': 'DEPT001', 'departmentCode': 'IT', 'departmentName': 'Information Technology'},
    {'departmentId': 'DEPT002', 'departmentCode': 'BUS', 'departmentName': 'Business Administration'},
    {'departmentId': 'DEPT003', 'departmentCode': 'ENG', 'departmentName': 'Engineering'},
]

departments = {}
for dept_data in departments_data:
    dept, created = Department.objects.get_or_create(
        departmentId=dept_data['departmentId'],
        defaults=dept_data
    )
    departments[dept_data['departmentCode']] = dept
    if created:
        print(f"  ✓ Created: {dept.departmentName}")

# ============================================================================
# 2. TEACHERS
# ============================================================================
print("\n👨‍🏫 Step 2: Creating Teachers...")
teachers_data = [
    {'username': 'teacher1', 'teacherId': 'T001', 'teacherCode': 'IT001', 'dept': 'IT', 'name': 'Nguyen Van A'},
    {'username': 'teacher2', 'teacherId': 'T002', 'teacherCode': 'IT002', 'dept': 'IT', 'name': 'Tran Thi B'},
    {'username': 'teacher3', 'teacherId': 'T003', 'teacherCode': 'BUS001', 'dept': 'BUS', 'name': 'Prof. Mike Johnson'},
    {'username': 'teacher4', 'teacherId': 'T004', 'teacherCode': 'ENG001', 'dept': 'ENG', 'name': 'Dr. Sarah Wilson'},
]

teachers = {}
for t_data in teachers_data:
    user, created = User.objects.get_or_create(
        username=t_data['username'],
        defaults={
            'email': f"{t_data['username']}@test.com",
            'user_type': 'teacher',
            'full_name': t_data['name'],
            'password': make_password('python123'),
            'status': 'active'
        }
    )
    teacher, created = Teacher.objects.get_or_create(
        teacherId=t_data['teacherId'],
        defaults={
            'user': user,
            'teacherCode': t_data['teacherCode'],
            'department': departments[t_data['dept']],
            'position': 'Lecturer',
            'hireDate': date(2020, 1, 1)
        }
    )
    teachers[t_data['teacherCode']] = teacher
    if created:
        print(f"  ✓ Created: {t_data['name']} ({t_data['teacherCode']})")

# ============================================================================
# 3. MAJORS
# ============================================================================
print("\n🎓 Step 3: Creating Majors...")
majors_data = [
    {'majorId': 'MAJ001', 'majorCode': 'SE', 'majorName': 'Software Engineering', 'dept': 'IT'},
    {'majorId': 'MAJ002', 'majorCode': 'CS', 'majorName': 'Computer Science', 'dept': 'IT'},
    {'majorId': 'MAJ003', 'majorCode': 'BA', 'majorName': 'Business Administration', 'dept': 'BUS'},
    {'majorId': 'MAJ004', 'majorCode': 'CE', 'majorName': 'Civil Engineering', 'dept': 'ENG'},
]

majors = {}
for maj_data in majors_data:
    major, created = Major.objects.get_or_create(
        majorId=maj_data['majorId'],
        defaults={
            'majorCode': maj_data['majorCode'],
            'majorName': maj_data['majorName'],
            'department': departments[maj_data['dept']],
            'durationYears': 4,
            'totalCredits': 140
        }
    )
    majors[maj_data['majorCode']] = major
    if created:
        print(f"  ✓ Created: {major.majorName}")

# ============================================================================
# 4. STUDENT CLASSES
# ============================================================================
print("\n🏫 Step 4: Creating Student Classes...")
classes_data = [
    {'classId': 'CL001', 'classCode': 'SE2024A', 'className': 'Software Engineering 2024A', 'major': 'SE'},
    {'classId': 'CL002', 'classCode': 'SE2024B', 'className': 'Software Engineering 2024B', 'major': 'SE'},
    {'classId': 'CL003', 'classCode': 'CS2024A', 'className': 'Computer Science 2024A', 'major': 'CS'},
    {'classId': 'CL004', 'classCode': 'BA2024A', 'className': 'Business Administration 2024A', 'major': 'BA'},
]

student_classes = {}
for cl_data in classes_data:
    student_class, created = StudentClass.objects.get_or_create(
        classId=cl_data['classId'],
        defaults={
            'classCode': cl_data['classCode'],
            'className': cl_data['className'],
            'major': majors[cl_data['major']],
            'academicYear': '2024-2025',
            'advisorTeacher': teachers['IT001'],
            'maxStudents': 30,
            'currentStudents': 0
        }
    )
    student_classes[cl_data['classCode']] = student_class
    if created:
        print(f"  ✓ Created: {student_class.className}")

# ============================================================================
# 5. STUDENTS
# ============================================================================
print("\n👨‍🎓 Step 5: Creating Students...")
students_data = []
for i in range(1, 21):  # Create 20 students
    username = f'student{i}'
    user, _ = User.objects.get_or_create(
        username=username,
        defaults={
            'email': f'{username}@test.com',
            'user_type': 'student',
            'full_name': f'Student {i}',
            'phone': f'032{i:07d}',
            'password': make_password('python123'),
            'status': 'active'
        }
    )
    students_data.append({
        'username': username,
        'studentId': f'S{i:03d}',
        'studentCode': f'SE{i:03d}',
        'class': random.choice(['SE2024A', 'SE2024B', 'CS2024A', 'BA2024A'])
    })

students = {}
for s_data in students_data:
    try:
        student = Student.objects.get(studentId=s_data['studentId'])
    except Student.DoesNotExist:
        user = User.objects.get(username=s_data['username'])
        student, created = Student.objects.get_or_create(
            studentId=s_data['studentId'],
            defaults={
                'user': user,
                'studentCode': s_data['studentCode'],
                'studentClass': student_classes[s_data['class']],
                'dateOfBirth': date(2000, 1, 1),
                'gender': random.choice(['male', 'female']),
                'enrollmentYear': 2024,
                'gpa': Decimal('0.0'),
                'totalCredits': 0
            }
        )
        if created:
            # Update currentStudents count
            student.studentClass.currentStudents += 1
            student.studentClass.save()
    students[s_data['studentCode']] = student

print(f"  ✓ Created/Found {len(students)} students")

# ============================================================================
# 6. SUBJECTS
# ============================================================================
print("\n📚 Step 6: Creating Subjects...")
subjects_data = [
    {'subjectId': 'SUB001', 'subjectCode': 'CS101', 'subjectName': 'Introduction to Programming', 'dept': 'IT', 'credits': 3},
    {'subjectId': 'SUB002', 'subjectCode': 'CS102', 'subjectName': 'Data Structures', 'dept': 'IT', 'credits': 3},
    {'subjectId': 'SUB003', 'subjectCode': 'CS103', 'subjectName': 'Database Systems', 'dept': 'IT', 'credits': 4},
    {'subjectId': 'SUB004', 'subjectCode': 'CS104', 'subjectName': 'Web Development', 'dept': 'IT', 'credits': 3},
    {'subjectId': 'SUB005', 'subjectCode': 'CS201', 'subjectName': 'Advanced Programming', 'dept': 'IT', 'credits': 4},
    {'subjectId': 'SUB006', 'subjectCode': 'BUS101', 'subjectName': 'Business Management', 'dept': 'BUS', 'credits': 3},
    {'subjectId': 'SUB007', 'subjectCode': 'ENG101', 'subjectName': 'Engineering Mathematics', 'dept': 'ENG', 'credits': 4},
]

subjects = {}
for sub_data in subjects_data:
    subject, created = Subject.objects.get_or_create(
        subjectId=sub_data['subjectId'],
        defaults={
            'subjectCode': sub_data['subjectCode'],
            'subjectName': sub_data['subjectName'],
            'department': departments[sub_data['dept']],
            'credits': sub_data['credits'],
            'theoryHours': 30,
            'practiceHours': 15
        }
    )
    subjects[sub_data['subjectCode']] = subject
    if created:
        print(f"  ✓ Created: {subject.subjectName} ({subject.subjectCode})")

# ============================================================================
# 7. ACADEMIC YEAR & SEMESTER
# ============================================================================
print("\n📅 Step 7: Creating Academic Year & Semester...")
academic_year, created = AcademicYear.objects.get_or_create(
    yearId='AY2024',
    defaults={
        'yearCode': '2024-2025',
        'yearName': 'Academic Year 2024-2025',
        'startDate': date(2024, 9, 1),
        'endDate': date(2025, 6, 30),
        'status': 'active'
    }
)
if created:
    print(f"  ✓ Created: {academic_year.yearName}")

semester, created = Semester.objects.get_or_create(
    semesterId='SEM001',
    defaults={
        'semesterCode': '2024-1',
        'semesterName': 'Semester 1 - 2024',
        'academicYear': academic_year,
        'startDate': date(2024, 9, 1),
        'endDate': date(2024, 12, 31),
        'registrationStart': datetime(2024, 8, 15, 8, 0),
        'registrationEnd': datetime(2024, 8, 30, 17, 0),
        'status': 'active'
    }
)
if created:
    print(f"  ✓ Created: {semester.semesterName}")

# ============================================================================
# 8. COURSE CLASSES
# ============================================================================
print("\n📖 Step 8: Creating Course Classes...")
course_classes_data = [
    {'courseClassId': 'CC001', 'courseCode': 'CS101-01', 'courseName': 'Programming Fundamentals - Class 1', 'subject': 'CS101', 'teacher': 'IT001'},
    {'courseClassId': 'CC002', 'courseCode': 'CS102-01', 'courseName': 'Data Structures - Class 1', 'subject': 'CS102', 'teacher': 'IT002'},
    {'courseClassId': 'CC003', 'courseCode': 'CS103-01', 'courseName': 'Database Systems - Class 1', 'subject': 'CS103', 'teacher': 'IT001'},
    {'courseClassId': 'CC004', 'courseCode': 'CS104-01', 'courseName': 'Web Development - Class 1', 'subject': 'CS104', 'teacher': 'IT002'},
    {'courseClassId': 'CC005', 'courseCode': 'CS201-01', 'courseName': 'Advanced Programming - Class 1', 'subject': 'CS201', 'teacher': 'IT001'},
]

course_classes = {}
for cc_data in course_classes_data:
    max_students = random.randint(20, 30)
    current_students = random.randint(0, max_students - 5)
    
    course_class, created = CourseClass.objects.get_or_create(
        courseClassId=cc_data['courseClassId'],
        defaults={
            'courseCode': cc_data['courseCode'],
            'courseName': cc_data['courseName'],
            'subject': subjects[cc_data['subject']],
            'teacher': teachers[cc_data['teacher']],
            'semester': semester,
            'room': f'Room {random.randint(200, 500)}',
            'maxStudents': max_students,
            'currentStudents': current_students,
            'status': True
        }
    )
    if not created:
        # Update existing
        course_class.maxStudents = max_students
        course_class.currentStudents = current_students
        course_class.save()
    
    course_classes[cc_data['courseCode']] = course_class
    if created:
        print(f"  ✓ Created: {course_class.courseName} - Available: {max_students - current_students}/{max_students}")

# ============================================================================
# 9. COURSE REGISTRATIONS
# ============================================================================
print("\n📋 Step 9: Creating Course Registrations...")
registration_count = 0
for i, student_code in enumerate(list(students.keys())[:15]):
    student = students[student_code]
    # Register 2-3 courses
    random_classes = random.sample(list(course_classes.items()), random.randint(2, 3))
    
    for j, (course_code, course_class) in enumerate(random_classes):
        registration, created = CourseRegistration.objects.get_or_create(
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
            registration_count += 1
            # Update currentStudents
            course_class.currentStudents += 1
            course_class.save()

print(f"  ✓ Created {registration_count} registrations")

# ============================================================================
# 10. GRADES
# ============================================================================
print("\n📊 Step 10: Creating Grades...")
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

# Create grades for first 10 students
for i, student_code in enumerate(list(students.keys())[:10]):
    student = students[student_code]
    
    # Get student's registered courses
    registrations = CourseRegistration.objects.filter(
        student=student,
        semester=semester,
        status='registered'
    )[:3]  # Get up to 3 courses
    
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

print(f"  ✓ Created {grade_count} grades")

# ============================================================================
# 11. DOCUMENT TYPES
# ============================================================================
print("\n📄 Step 11: Creating Document Types...")
doc_types_data = [
    {'documentTypeId': 'DT001', 'name': 'Transcript', 'code': 'TRANSCRIPT', 'days': 7},
    {'documentTypeId': 'DT002', 'name': 'Certificate', 'code': 'CERT', 'days': 5},
    {'documentTypeId': 'DT003', 'name': 'Enrollment Letter', 'code': 'ENROLL', 'days': 3},
]

doc_types = {}
for dt_data in doc_types_data:
    doc_type, created = DocumentType.objects.get_or_create(
        documentTypeId=dt_data['documentTypeId'],
        defaults={
            'name': dt_data['name'],
            'code': dt_data['code'],
            'description': f'{dt_data["name"]} document',
            'maxRequestsPerSemester': 3,
            'processingDays': dt_data['days'],
            'status': 'active'
        }
    )
    doc_types[dt_data['code']] = doc_type
    if created:
        print(f"  ✓ Created: {doc_type.name}")

# ============================================================================
# 12. DOCUMENT REQUESTS
# ============================================================================
print("\n📝 Step 12: Creating Document Requests...")
request_statuses = ['pending', 'approved', 'completed']
doc_request_count = 0

for i, student_code in enumerate(list(students.keys())[:10]):
    student = students[student_code]
    doc_type = random.choice(list(doc_types.values()))
    status = random.choice(request_statuses)
    
    request_date = date.today() - timedelta(days=random.randint(1, 30))
    
    # Check if already exists
    existing = DocumentRequest.objects.filter(
        student=student,
        documentType=doc_type,
        semester=semester,
        status__in=['pending', 'approved', 'completed']
    ).first()
    
    if not existing:
        doc_request = DocumentRequest.objects.create(
            requestId=f'DR{i+1:06d}',
            student=student,
            documentType=doc_type,
            semester=semester,
            requestDate=datetime.combine(request_date, datetime.min.time()),
            purpose=f'Request for {doc_type.name.lower()}',
            status=status
        )
        doc_request_count += 1
        if status == 'approved' and random.choice([True, False]):
            doc_request.approvedDate = datetime.now() - timedelta(days=random.randint(1, 10))
            doc_request.save()

print(f"  ✓ Created {doc_request_count} document requests")

# ============================================================================
# 13. NOTIFICATIONS WITH RECIPIENTS
# ============================================================================
print("\n🔔 Step 13: Creating Notifications...")
master_user = get_or_create_master_user()

notifications_data = [
    {
        'notificationId': 'NOT001', 
        'title': 'Welcome New Students', 
        'content': 'Welcome to the new academic year! Please check your class schedule and course registration.',
        'notificationType': 'general',
        'priority': 1
    },
    {
        'notificationId': 'NOT002', 
        'title': 'Exam Schedule', 
        'content': 'Final exam schedule is now available. Please check the notice board.',
        'notificationType': 'academic',
        'priority': 2
    },
    {
        'notificationId': 'NOT003', 
        'title': 'Registration Reminder', 
        'content': 'Course registration deadline is approaching. Please register your courses before the deadline.',
        'notificationType': 'administrative',
        'priority': 3
    },
]

for not_data in notifications_data:
    notification, created = Notification.objects.get_or_create(
        notificationId=not_data['notificationId'],
        defaults={
            'createdBy': master_user,
            'title': not_data['title'],
            'content': not_data['content'],
            'targetAudience': 'all',
            'targetId': '[]',
            'notificationType': not_data['notificationType'],
            'priority': not_data['priority'],
            'status': 'active'
        }
    )
    if created:
        print(f"  ✓ Created: {notification.title}")
        
        # Create notification recipients for first 15 students
        for student_code in list(students.keys())[:15]:
            student = students[student_code]
            NotificationRecipient.objects.get_or_create(
                recipientId=f'{notification.notificationId}_{student.user.username}',
                defaults={
                    'notification': notification,
                    'user': student.user,
                    'deliveryStatus': 'delivered',
                    'deliveredAt': datetime.now() - timedelta(days=random.randint(0, 7))
                }
            )

# ============================================================================
# 14. TUITION FEES
# ============================================================================
print("\n💰 Step 14: Creating Tuition Fees...")
payment_statuses = ['unpaid', 'partial_paid', 'paid']
tuition_count = 0

for student_code in list(students.keys())[:15]:
    student = students[student_code]
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
    
    tuition, created = TuitionFee.objects.get_or_create(
        tuitionFee=f'TF{student.studentId}',
        defaults={
            'student': student,
            'semester': semester,
            'totalCredit': total_credit,
            'feePerCredit': fee_per_credit,
            'totalAmount': total_amount,
            'paidAmount': paid_amount,
            'paymentStatus': payment_status,
            'dueDate': date.today() + timedelta(days=30)
        }
    )
    if created:
        tuition_count += 1

print(f"  ✓ Created {tuition_count} tuition fees")

# ============================================================================
# 15. SUBJECT PREREQUISITES
# ============================================================================
print("\n📚 Step 15: Setting up Subject Prerequisites...")
# CS102 requires CS101
if subjects.get('CS101') and subjects.get('CS102'):
    subjects['CS102'].prerequisites.add(subjects['CS101'])
    
# CS201 requires CS101 and CS102
if subjects.get('CS201') and subjects.get('CS101') and subjects.get('CS102'):
    subjects['CS201'].prerequisites.add(subjects['CS101'])
    subjects['CS201'].prerequisites.add(subjects['CS102'])
    print("  ✓ CS102 requires CS101")
    print("  ✓ CS201 requires CS101 and CS102")

# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "=" * 60)
print("✅ Sample Data Creation Completed!")
print("=" * 60)
print(f"\n📊 Summary:")
print(f"  - Departments: {Department.objects.count()}")
print(f"  - Teachers: {Teacher.objects.count()}")
print(f"  - Students: {Student.objects.count()}")
print(f"  - Majors: {Major.objects.count()}")
print(f"  - Subjects: {Subject.objects.count()}")
print(f"  - Course Classes: {CourseClass.objects.count()}")
print(f"  - Grades: {Grade.objects.count()}")
print(f"  - Registrations: {CourseRegistration.objects.count()}")
print(f"  - Document Requests: {DocumentRequest.objects.count()}")
print(f"  - Document Types: {DocumentType.objects.count()}")
print(f"  - Notifications: {Notification.objects.count()}")
print(f"  - Notification Recipients: {NotificationRecipient.objects.count()}")
print(f"  - Tuition Fees: {TuitionFee.objects.count()}")

print(f"\n🔑 Test Credentials:")
print(f"  - Student: username='student1' to 'student20', password='python123'")
print(f"  - Teacher: username='teacher1' to 'teacher4', password='python123'")
print(f"  - Master Admin: username='master', password='master123'")

print("\n" + "=" * 60)
