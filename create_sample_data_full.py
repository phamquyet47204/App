import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_management.settings')
django.setup()

from core.models import *
from django.contrib.auth.hashers import make_password
from datetime import datetime, date
from decimal import Decimal
import random

print("Creating sample data...")

# 1. Create Departments
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
    print(f"Department: {dept.departmentName}")

# 2. Create Teachers
teachers_data = [
    {'username': 'teacher1', 'teacherId': 'T001', 'teacherCode': 'IT001', 'dept': 'IT', 'name': 'Dr. John Smith'},
    {'username': 'teacher2', 'teacherId': 'T002', 'teacherCode': 'IT002', 'dept': 'IT', 'name': 'Dr. Jane Doe'},
    {'username': 'teacher3', 'teacherId': 'T003', 'teacherCode': 'BUS001', 'dept': 'BUS', 'name': 'Prof. Mike Johnson'},
    {'username': 'teacher4', 'teacherId': 'T004', 'teacherCode': 'ENG001', 'dept': 'ENG', 'name': 'Dr. Sarah Wilson'},
]

teachers = {}
for t_data in teachers_data:
    # Create user if not exists
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
    print(f"Teacher: {teacher.user.full_name}")

# 3. Create Majors
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
    print(f"Major: {major.majorName}")

# 4. Create Student Classes
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
    print(f"Class: {student_class.className}")

# 5. Create Students
students_data = []

# Create students 1-20
for i in range(1, 21):
    User.objects.get_or_create(
        username=f'student{i}',
        defaults={
            'email': f'student{i}@test.com',
            'user_type': 'student',
            'full_name': f'Student {i}',
            'password': make_password('python123'),
            'status': 'active'
        }
    )
    students_data.append({
        'username': f'student{i}',
        'studentId': f'S{i:03d}',
        'studentCode': f'SE{i:03d}',
        'class': random.choice(['SE2024A', 'SE2024B', 'CS2024A'])
    })

students = {}
for s_data in students_data:
    user = User.objects.get(username=s_data['username'])
    student, created = Student.objects.get_or_create(
        studentId=s_data['studentId'],
        defaults={
            'user': user,
            'studentCode': s_data['studentCode'],
            'studentClass': student_classes[s_data['class']],
            'dateOfBirth': date(2000, 1, 1),
            'gender': 'male',
            'enrollmentYear': 2024,
            'gpa': Decimal('0.0'),
            'totalCredits': 0
        }
    )
    students[s_data['studentCode']] = student
    print(f"Student: {student.user.full_name}")

# 6. Create Subjects
subjects_data = [
    {'subjectId': 'SUB001', 'subjectCode': 'CS101', 'subjectName': 'Programming Fundamentals', 'dept': 'IT', 'credits': 3},
    {'subjectId': 'SUB002', 'subjectCode': 'CS102', 'subjectName': 'Data Structures', 'dept': 'IT', 'credits': 3},
    {'subjectId': 'SUB003', 'subjectCode': 'CS103', 'subjectName': 'Database Systems', 'dept': 'IT', 'credits': 4},
    {'subjectId': 'SUB004', 'subjectCode': 'CS104', 'subjectName': 'Web Development', 'dept': 'IT', 'credits': 3},
    {'subjectId': 'SUB005', 'subjectCode': 'BUS101', 'subjectName': 'Business Management', 'dept': 'BUS', 'credits': 3},
    {'subjectId': 'SUB006', 'subjectCode': 'ENG101', 'subjectName': 'Engineering Mathematics', 'dept': 'ENG', 'credits': 4},
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
    print(f"Subject: {subject.subjectName}")

# 7. Create Academic Year & Semester
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
print(f"Semester: {semester.semesterName}")

# 8. Create Course Classes
course_classes_data = [
    {'courseClassId': 'CC001', 'courseCode': 'CS101-01', 'courseName': 'Programming Fundamentals - Class 1', 'subject': 'CS101', 'teacher': 'IT001'},
    {'courseClassId': 'CC002', 'courseCode': 'CS102-01', 'courseName': 'Data Structures - Class 1', 'subject': 'CS102', 'teacher': 'IT002'},
    {'courseClassId': 'CC003', 'courseCode': 'CS103-01', 'courseName': 'Database Systems - Class 1', 'subject': 'CS103', 'teacher': 'IT001'},
    {'courseClassId': 'CC004', 'courseCode': 'CS104-01', 'courseName': 'Web Development - Class 1', 'subject': 'CS104', 'teacher': 'IT002'},
]

course_classes = {}
for cc_data in course_classes_data:
    course_class, created = CourseClass.objects.get_or_create(
        courseClassId=cc_data['courseClassId'],
        defaults={
            'courseCode': cc_data['courseCode'],
            'courseName': cc_data['courseName'],
            'subject': subjects[cc_data['subject']],
            'teacher': teachers[cc_data['teacher']],
            'semester': semester,
            'room': f'Room {random.randint(101, 999)}',
            'maxStudents': 25,
            'currentStudents': 0
        }
    )
    course_classes[cc_data['courseCode']] = course_class
    print(f"Course Class: {course_class.courseName}")

# 9. Create Course Registrations
for i, student_code in enumerate(list(students.keys())[:10]):
    for j, course_code in enumerate(list(course_classes.keys())[:2]):
        registration, created = CourseRegistration.objects.get_or_create(
            registrationId=f'REG{i:03d}{j:03d}',
            defaults={
                'student': students[student_code],
                'courseClass': course_classes[course_code],
                'semester': semester,
                'registrationDate': date(2024, 8, 20),
                'status': 'registered'
            }
        )
        if created:
            print(f"Registration: {student_code} -> {course_code}")

# 10. Create Grades
grade_letters = ['A', 'B', 'C', 'D', 'F']
grade_points = [4.0, 3.0, 2.0, 1.0, 0.0]

for i, student_code in enumerate(list(students.keys())[:10]):
    for j, (course_code, subject_code) in enumerate(zip(list(course_classes.keys())[:2], ['CS101', 'CS102'])):
        grade_idx = random.randint(0, 4)
        grade, created = Grade.objects.get_or_create(
            gradeId=f'GR{i:03d}{j:03d}',
            defaults={
                'student': students[student_code],
                'subject': subjects[subject_code],
                'teacher': teachers['IT001'],
                'courseClass': course_classes[course_code],
                'semester': semester,
                'assginmentscore': Decimal(str(random.uniform(7.0, 10.0))),
                'midterm_score': Decimal(str(random.uniform(6.0, 9.5))),
                'final_score': Decimal(str(random.uniform(6.5, 9.8))),
                'average_score': Decimal(str(random.uniform(6.8, 9.2))),
                'letterGrade': grade_letters[grade_idx],
                'gradePoint': Decimal(str(grade_points[grade_idx])),
                'isPassed': grade_idx < 4
            }
        )
        if created:
            print(f"Grade: {student_code} - {subject_code} - {grade.letterGrade}")

# 11. Create Document Types
doc_types_data = [
    {'documentTypeId': 'DT001', 'name': 'Transcript', 'code': 'TRANSCRIPT'},
    {'documentTypeId': 'DT002', 'name': 'Certificate', 'code': 'CERT'},
    {'documentTypeId': 'DT003', 'name': 'Enrollment Letter', 'code': 'ENROLL'},
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
            'processingDays': 7
        }
    )
    doc_types[dt_data['code']] = doc_type
    print(f"Document Type: {doc_type.name}")

# 12. Create Tuition Fees
for i, student_code in enumerate(list(students.keys())[:5]):
    tuition, created = TuitionFee.objects.get_or_create(
        tuitionFee=f'TF{i:03d}',
        defaults={
            'student': students[student_code],
            'semester': semester,
            'totalCredit': 12,
            'feePerCredit': Decimal('500000'),
            'totalAmount': Decimal('6000000'),
            'paidAmount': Decimal('3000000'),
            'paymentStatus': 'partial_paid',
            'dueDate': date(2024, 10, 15)
        }
    )
    if created:
        print(f"Tuition Fee: {student_code} - {tuition.totalAmount}")

# 13. Create Notifications
notifications_data = [
    {'notificationId': 'NOT001', 'title': 'Welcome New Students', 'content': 'Welcome to new academic year!'},
    {'notificationId': 'NOT002', 'title': 'Exam Schedule', 'content': 'Final exam schedule is now available.'},
    {'notificationId': 'NOT003', 'title': 'Registration Reminder', 'content': 'Course registration deadline is approaching.'},
]

for not_data in notifications_data:
    notification, created = Notification.objects.get_or_create(
        notificationId=not_data['notificationId'],
        defaults={
            'createdBy': User.objects.get(username='master'),
            'title': not_data['title'],
            'content': not_data['content'],
            'targetAudience': 'all',
            'notificationType': 'general',
            'priority': 1
        }
    )
    if created:
        print(f"Notification: {notification.title}")

print("\n✅ Sample data created successfully!")
print(f"📊 Summary:")
print(f"- Departments: {Department.objects.count()}")
print(f"- Teachers: {Teacher.objects.count()}")
print(f"- Students: {Student.objects.count()}")
print(f"- Majors: {Major.objects.count()}")
print(f"- Subjects: {Subject.objects.count()}")
print(f"- Course Classes: {CourseClass.objects.count()}")
print(f"- Grades: {Grade.objects.count()}")
print(f"- Registrations: {CourseRegistration.objects.count()}")
print(f"- Tuition Fees: {TuitionFee.objects.count()}")
print(f"- Notifications: {Notification.objects.count()}")