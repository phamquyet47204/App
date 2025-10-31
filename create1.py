import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_management.settings')
django.setup()

from core.models import *
from django.contrib.auth.hashers import make_password
from datetime import datetime, date, timedelta
from decimal import Decimal
import random

print("Creating sample data for student endpoints...")

# Helper function to get or create a master user for notifications
def get_or_create_master_user():
    master_user, created = User.objects.get_or_create(
        username='master',
        defaults={
            'email': 'master@university.com',
            'user_type': 'admin',
            'full_name': 'System Master',
            'password': make_password('master123'),
            'status': 'active'
        }
    )
    return master_user

# 1. ENSURE DEPARTMENTS EXIST
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

# 2. ENSURE TEACHERS EXIST
teachers_data = [
    {'username': 'teacher1', 'teacherId': 'T001', 'teacherCode': 'IT001', 'dept': 'IT', 'name': 'Dr. John Smith'},
    {'username': 'teacher2', 'teacherId': 'T002', 'teacherCode': 'IT002', 'dept': 'IT', 'name': 'Dr. Jane Doe'},
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

# 3. ENSURE MAJORS EXIST
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

# 4. ENSURE STUDENT CLASSES EXIST
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

# 5. ENSURE STUDENTS EXIST
students_data = []
for i in range(1, 51):  # Create 50 students
    user, _ = User.objects.get_or_create(
        username=f'student{i}',
        defaults={
            'email': f'student{i}@test.com',
            'user_type': 'student',
            'full_name': f'Student {i}',
            'phone': f'090{i:06d}',
            'password': make_password('python123'),
            'status': 'active'
        }
    )
    students_data.append({
        'username': f'student{i}',
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
    students[s_data['studentCode']] = student

# 6. ENSURE SUBJECTS EXIST
subjects_data = [
    {'subjectId': 'SUB001', 'subjectCode': 'CS101', 'subjectName': 'Programming Fundamentals', 'dept': 'IT', 'credits': 3},
    {'subjectId': 'SUB002', 'subjectCode': 'CS102', 'subjectName': 'Data Structures', 'dept': 'IT', 'credits': 3},
    {'subjectId': 'SUB003', 'subjectCode': 'CS103', 'subjectName': 'Database Systems', 'dept': 'IT', 'credits': 4},
    {'subjectId': 'SUB004', 'subjectCode': 'CS104', 'subjectName': 'Web Development', 'dept': 'IT', 'credits': 3},
    {'subjectId': 'SUB005', 'subjectCode': 'CS201', 'subjectName': 'Advanced Programming', 'dept': 'IT', 'credits': 4},
    {'subjectId': 'SUB006', 'subjectCode': 'BUS101', 'subjectName': 'Business Management', 'dept': 'BUS', 'credits': 3},
    {'subjectId': 'SUB007', 'subjectCode': 'ENG101', 'subjectName': 'Engineering Mathematics', 'dept': 'ENG', 'credits': 4},
]

subjects = {}
for sub_data in subjects_data:
    try:
        subject = Subject.objects.get(subjectCode=sub_data['subjectCode'])
        print(f"  Using existing: {subject.subjectName}")
    except Subject.DoesNotExist:
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

# 7. ENSURE ACADEMIC YEAR & SEMESTER EXIST
academic_year, created = AcademicYear.objects.get_or_create(
    yearId='AY2024',
    defaults={
        'yearCode': '2024-2025',
        'yearName': 'Academic Year 2024-2025',
        'startDate': date(2024, 9, 1),
        'endDate': date(2025, 6, 30)
    }
)

semester, created = Semester.objects.get_or_create(
    semesterId='SEM001',
    defaults={
        'semesterCode': '2024-1',
        'semesterName': 'Semester 1 - 2024',
        'academicYear': academic_year,
        'startDate': date(2024, 9, 1),
        'endDate': date(2024, 12, 31),
        'registrationStart': datetime(2024, 8, 15, 8, 0),
        'registrationEnd': datetime(2024, 8, 30, 17, 0)
    }
)

# Create additional semesters
semester2, created = Semester.objects.get_or_create(
    semesterId='SEM002',
    defaults={
        'semesterCode': '2024-2',
        'semesterName': 'Semester 2 - 2024',
        'academicYear': academic_year,
        'startDate': date(2025, 1, 1),
        'endDate': date(2025, 5, 31),
        'registrationStart': datetime(2024, 12, 15, 8, 0),
        'registrationEnd': datetime(2024, 12, 30, 17, 0)
    }
)

print(f"✓ Using Semester: {semester.semesterName}")

# 8. CREATE COURSE CLASSES (for GET /api/crud/course-classes/)
print("\n📚 Creating Course Classes...")
course_classes_data = [
    {'courseClassId': 'CC001', 'courseCode': 'CS101-01', 'courseName': 'Programming Fundamentals - Class 1', 'subject': 'CS101', 'teacher': 'IT001'},
    {'courseClassId': 'CC002', 'courseCode': 'CS102-01', 'courseName': 'Data Structures - Class 1', 'subject': 'CS102', 'teacher': 'IT002'},
    {'courseClassId': 'CC003', 'courseCode': 'CS103-01', 'courseName': 'Database Systems - Class 1', 'subject': 'CS103', 'teacher': 'IT001'},
    {'courseClassId': 'CC004', 'courseCode': 'CS104-01', 'courseName': 'Web Development - Class 1', 'subject': 'CS104', 'teacher': 'IT002'},
    {'courseClassId': 'CC005', 'courseCode': 'CS201-01', 'courseName': 'Advanced Programming - Class 1', 'subject': 'CS201', 'teacher': 'IT001'},
    {'courseClassId': 'CC006', 'courseCode': 'CS101-02', 'courseName': 'Programming Fundamentals - Class 2', 'subject': 'CS101', 'teacher': 'IT002'},
    {'courseClassId': 'CC007', 'courseCode': 'CS102-02', 'courseName': 'Data Structures - Class 2', 'subject': 'CS102', 'teacher': 'IT001'},
]

course_classes = {}
for cc_data in course_classes_data:
    max_students = random.randint(20, 30)
    current_students = random.randint(5, max_students - 5)
    
    try:
        course_class = CourseClass.objects.get(courseClassId=cc_data['courseClassId'])
        # Update existing
        course_class.maxStudents = max_students
        course_class.currentStudents = current_students
        course_class.save()
    except CourseClass.DoesNotExist:
        course_class, created = CourseClass.objects.get_or_create(
            courseClassId=cc_data['courseClassId'],
            defaults={
                'courseCode': cc_data['courseCode'],
                'courseName': cc_data['courseName'],
                'subject': subjects[cc_data['subject']],
                'teacher': teachers[cc_data['teacher']],
                'semester': semester,
                'room': f'Room {random.randint(101, 999)}',
                'maxStudents': max_students,
                'currentStudents': current_students
            }
        )
    course_classes[cc_data['courseCode']] = course_class
    print(f"  ✓ {course_class.courseName} - Available: {max_students - current_students}/{max_students}")

# 9. CREATE GRADES (for GET /api/student/my-grades/)
print("\n📊 Creating Grades...")
grade_letters = ['A', 'B', 'C', 'D', 'F']
grade_points = [4.0, 3.0, 2.0, 1.0, 0.0]

# Create grades for first 20 students
for i, student_code in enumerate(list(students.keys())[:20]):
    student = students[student_code]
    
    # Get 2-3 random course classes for each student
    random_classes = random.sample(list(course_classes.items()), random.randint(2, 3))
    
    for j, (course_code, course_class) in enumerate(random_classes):
        subject = course_class.subject
        grade_idx = random.randint(0, 3)  # Avoid F grades for most students
        
        grade, created = Grade.objects.get_or_create(
            gradeId=f'GR{student.studentId}{j+1:02d}',
            defaults={
                'student': student,
                'subject': subject,
                'teacher': course_class.teacher,
                'courseClass': course_class,
                'semester': semester,
                'assginmentscore': Decimal(str(random.uniform(7.0, 10.0))),
                'midterm_score': Decimal(str(random.uniform(6.0, 9.5))),
                'final_score': Decimal(str(random.uniform(6.5, 9.8))),
                'average_score': Decimal(str(random.uniform(7.0, 9.0))),
                'letterGrade': grade_letters[grade_idx],
                'gradePoint': Decimal(str(grade_points[grade_idx])),
                'isPassed': True
            }
        )
        if created:
            print(f"  ✓ {student_code} - {subject.subjectCode}: {grade.letterGrade} ({grade.average_score:.1f})")

# 10. CREATE DOCUMENT TYPES
print("\n📄 Creating Document Types...")
doc_types_data = [
    {'documentTypeId': 'DT001', 'name': 'Transcript', 'code': 'TRANSCRIPT', 'days': 7},
    {'documentTypeId': 'DT002', 'name': 'Certificate', 'code': 'CERT', 'days': 5},
    {'documentTypeId': 'DT003', 'name': 'Enrollment Letter', 'code': 'ENROLL', 'days': 3},
    {'documentTypeId': 'DT004', 'name': 'Confirmation Letter', 'code': 'CONFIRM', 'days': 3},
]

doc_types = {}
for dt_data in doc_types_data:
    try:
        doc_type = DocumentType.objects.get(code=dt_data['code'])
    except DocumentType.DoesNotExist:
        doc_type, created = DocumentType.objects.get_or_create(
            documentTypeId=dt_data['documentTypeId'],
            defaults={
                'name': dt_data['name'],
                'code': dt_data['code'],
                'description': f'{dt_data["name"]} document',
                'maxRequestsPerSemester': 3,
                'processingDays': dt_data['days']
            }
        )
    doc_types[dt_data['code']] = doc_type
    print(f"  ✓ {doc_type.name}")

# 11. CREATE DOCUMENT REQUESTS (for GET /api/crud/document-requests/)
print("\n📝 Creating Document Requests...")
request_statuses = ['pending', 'approved', 'completed', 'rejected']
for i, student_code in enumerate(list(students.keys())[:15]):
    student = students[student_code]
    doc_type = random.choice(list(doc_types.values()))
    status = random.choice(request_statuses)
    
    request_date = date.today() - timedelta(days=random.randint(1, 30))
    
    doc_request, created = DocumentRequest.objects.get_or_create(
        requestId=f'DOC{student.studentId}{i+1:02d}',
        defaults={
            'semester': semester,
            'requestDate': datetime.combine(request_date, datetime.min.time()),
            'purpose': f'Request for {doc_type.name.lower()}',
            'status': status,
            'documentType': doc_type
        }
    )
    if created:
        doc_request.student.add(student)
        print(f"  ✓ {student_code}: {doc_type.name} - {status}")

# 12. CREATE NOTIFICATIONS WITH RECIPIENTS (for GET /api/services/notifications/unread/)
print("\n🔔 Creating Notifications...")
master_user = get_or_create_master_user()

notifications_data = [
    {
        'notificationId': 'NOT001', 
        'title': 'Welcome New Students', 
        'content': 'Welcome to the new academic year! Please check your class schedule and course registration.',
        'notificationType': 'general',
        'priority': 'normal'
    },
    {
        'notificationId': 'NOT002', 
        'title': 'Final Exam Schedule Available', 
        'content': 'The final exam schedule for Semester 1 is now available. Please check the notice board.',
        'notificationType': 'academic',
        'priority': 'high'
    },
    {
        'notificationId': 'NOT003', 
        'title': 'Course Registration Reminder', 
        'content': 'Course registration deadline is approaching. Please register your courses before the deadline.',
        'notificationType': 'administrative',
        'priority': 'urgent'
    },
    {
        'notificationId': 'NOT004', 
        'title': 'Library Hours Extended', 
        'content': 'Due to high demand during exam period, library hours have been extended to 10 PM.',
        'notificationType': 'general',
        'priority': 'normal'
    },
    {
        'notificationId': 'NOT005', 
        'title': 'Tuition Fee Payment Deadline', 
        'content': 'Reminder: Tuition fee payment deadline is October 15, 2024. Please make payment on time.',
        'notificationType': 'administrative',
        'priority': 'urgent'
    },
]

for not_data in notifications_data:
    notification, created = Notification.objects.get_or_create(
        notificationId=not_data['notificationId'],
        defaults={
            'createdBy': master_user,
            'title': not_data['title'],
            'content': not_data['content'],
            'targetAudience': 'student',
            'notificationType': not_data['notificationType'],
            'priority': {'normal': 1, 'high': 2, 'urgent': 3}.get(not_data['priority'], 1)
        }
    )
    if created:
        print(f"  ✓ {notification.title}")
        
        # Create notification recipients for first 30 students
        for i, student_code in enumerate(list(students.keys())[:30]):
            student = students[student_code]
            recipient, created = NotificationRecipient.objects.get_or_create(
                recipientId=f'{notification.notificationId}_{student.user.username}',
                defaults={
                    'notification': notification,
                    'user': student.user,
                    'deliveryStatus': 'delivered',
                    'deliveredAt': datetime.now() - timedelta(days=random.randint(0, 7))
                }
            )

# 13. CREATE TUITION FEES (for GET /api/crud/tuition-fees/)
print("\n💰 Creating Tuition Fees...")
payment_statuses = ['unpaid', 'partial_paid', 'paid']
for i, student_code in enumerate(list(students.keys())[:30]):
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
        print(f"  ✓ {student_code}: {total_credit} credits - {payment_status} - Due: {tuition.dueDate}")

# 14. CREATE COURSE REGISTRATIONS
print("\n📋 Creating Course Registrations...")
for i, student_code in enumerate(list(students.keys())[:30]):
    student = students[student_code]
    
    # Register 2-4 courses
    random_classes = random.sample(list(course_classes.items()), random.randint(2, 4))
    
    for j, (course_code, course_class) in enumerate(random_classes):
        registration, created = CourseRegistration.objects.get_or_create(
            registrationId=f'REG{student.studentId}{j+1:02d}',
            defaults={
                'student': student,
                'courseClass': course_class,
                'semester': semester,
                'registrationDate': date(2024, 8, random.randint(15, 30)),
                'status': 'registered'
            }
        )

# 15. CREATE SUBJECT PREREQUISITES (for prerequisites check)
print("\n📚 Setting up Subject Prerequisites...")
# CS102 requires CS101
if subjects.get('CS101') and subjects.get('CS102'):
    subjects['CS102'].prerequisites.add(subjects['CS101'])
    
# CS201 requires CS101 and CS102
if subjects.get('CS201') and subjects.get('CS101') and subjects.get('CS102'):
    subjects['CS201'].prerequisites.add(subjects['CS101'])
    subjects['CS201'].prerequisites.add(subjects['CS102'])
    print("  ✓ CS102 requires CS101")
    print("  ✓ CS201 requires CS101 and CS102")

print("\n✅ Sample data created successfully!")
print(f"\n📊 Summary:")
print(f"- Departments: {Department.objects.count()}")
print(f"- Teachers: {Teacher.objects.count()}")
print(f"- Students: {Student.objects.count()}")
print(f"- Majors: {Major.objects.count()}")
print(f"- Subjects: {Subject.objects.count()}")
print(f"- Course Classes: {CourseClass.objects.count()}")
print(f"- Grades: {Grade.objects.count()}")
print(f"- Registrations: {CourseRegistration.objects.count()}")
print(f"- Document Requests: {DocumentRequest.objects.count()}")
print(f"- Notifications: {Notification.objects.count()}")
print(f"- Notification Recipients: {NotificationRecipient.objects.count()}")
print(f"- Tuition Fees: {TuitionFee.objects.count()}")
print(f"\n🔑 Test Credentials:")
print(f"- Student Login: username='student1' to 'student50', password='python123'")
print(f"- Teacher Login: username='teacher1' to 'teacher4', password='python123'")

