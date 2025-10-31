import os, sys
import django

# ✅ Trỏ đúng vào project Django hiện tại
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_management.settings')

# ✅ Khởi tạo môi trường Django
django.setup()

# ✅ Import models
from university.models import (
    Department, Student, Teacher, Subject, Semester,
    CourseClass, CourseRegistration, Notification,
    NotificationRecipient, Grade
)


print(" Bắt đầu tạo dữ liệu mẫu...")

# -------------------------------
# 1️⃣ Tạo khoa (Department)
# -------------------------------
departments = ['Công nghệ thông tin', 'Kinh tế', 'Ngôn ngữ Anh', 'Khoa học dữ liệu']
department_objs = []
for name in departments:
    dept, _ = Department.objects.get_or_create(
        name=name,
        defaults={'description': f'Khoa {name}'}
    )
    department_objs.append(dept)
print(f"Đã tạo {len(department_objs)} khoa.")

# -------------------------------
# 2️⃣ Tạo user & student
# -------------------------------
students = []
for i in range(1, 6):
    username = f"student{i}"
    user, _ = User.objects.get_or_create(username=username)
    user.set_password('python123')
    user.save()

    dept = random.choice(department_objs)
    student, _ = Student.objects.get_or_create(
        studentId=f"S{i:03d}",
        defaults={
            'studentCode': f"SE{i:03d}",
            'user': user,
            'department': dept,
            'gpa': Decimal(str(round(random.uniform(2.0, 4.0), 2))),
            'totalCredits': random.randint(30, 120),
            'enrollmentYear': random.choice([2022, 2023, 2024]),
        }
    )
    students.append(student)
print(f"Đã tạo {len(students)} sinh viên.")

# -------------------------------
# 3️⃣ Tạo giảng viên
# -------------------------------
teachers = []
for i in range(1, 4):
    username = f"teacher{i}"
    user, _ = User.objects.get_or_create(username=username)
    user.set_password('python123')
    user.save()

    dept = random.choice(department_objs)
    teacher, _ = Teacher.objects.get_or_create(
        teacherId=f"T{i:03d}",
        defaults={
            'teacherCode': f"TC{i:03d}",
            'user': user,
            'department': dept,
            'specialization': "Giảng viên chính"
        }
    )
    teachers.append(teacher)
print(f"Đã tạo {len(teachers)} giảng viên.")

# -------------------------------
# 4️⃣ Tạo môn học (Subject)
# -------------------------------
subject_names = [
    "Toán cao cấp", "Cấu trúc dữ liệu", "Lập trình Python",
    "Cơ sở dữ liệu", "Kinh tế vi mô", "Tiếng Anh chuyên ngành"
]
subjects = []
for i, name in enumerate(subject_names, start=1):
    subj, _ = Subject.objects.get_or_create(
        subjectId=f"SUB{i:03d}",
        defaults={
            'subjectCode': f"SB{i:03d}",
            'subjectName': name,
            'credit': random.choice([2, 3, 4]),
            'department': random.choice(department_objs)
        }
    )
    subjects.append(subj)
print(f"Đã tạo {len(subjects)} môn học.")

# -------------------------------
# 5️⃣ Tạo học kỳ (Semester)
# -------------------------------
today = date.today()
semester1, _ = Semester.objects.get_or_create(
    semesterId="SEM001",
    defaults={
        "semesterName": "Học kỳ 1 - 2024",
        "startDate": today.replace(month=9, day=1),
        "endDate": today.replace(month=12, day=31)
    }
)
semester2, _ = Semester.objects.get_or_create(
    semesterId="SEM002",
    defaults={
        "semesterName": "Học kỳ 2 - 2025",
        "startDate": today.replace(month=2, day=1),
        "endDate": today.replace(month=5, day=31)
    }
)
current_semester = semester1 if today < semester2.startDate else semester2
print(f"Học kỳ hiện tại: {current_semester.semesterName}")

# -------------------------------
# 6️⃣ Tạo lớp học phần (CourseClass)
# -------------------------------
course_classes = []
for i in range(1, 7):
    subj = random.choice(subjects)
    teacher = random.choice(teachers)
    semester = random.choice([semester1, semester2])

    course_class, _ = CourseClass.objects.get_or_create(
        courseClassId=f"CC{i:03d}",
        defaults={
            "courseCode": f"CSE{i:03d}",
            "courseName": subj.subjectName,
            "subject": subj,
            "teacher": teacher,
            "semester": semester,
            "room": f"Phòng {random.randint(101, 999)}",
            "maxStudents": random.randint(30, 60),
            "currentStudents": 0,
            "dayOfWeek": random.choice(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']),
            "startTime": f"{random.choice([7, 9, 13])}:00",
            "endTime": f"{random.choice([9, 11, 15])}:00"
        }
    )
    course_classes.append(course_class)
print(f"Đã tạo {len(course_classes)} lớp học phần.")

# -------------------------------
# 7️⃣ Đăng ký môn học (CourseRegistration)
# -------------------------------
for student in students:
    registered = random.sample(course_classes, k=random.randint(2, 4))
    for c in registered:
        CourseRegistration.objects.get_or_create(
            student=student,
            courseClass=c,
            defaults={"registeredAt": datetime.now() - timedelta(days=random.randint(1, 10))}
        )
print(f"Sinh viên đã đăng ký lớp học phần.")

# -------------------------------
# 8️⃣ Tạo điểm (Grade)
# -------------------------------
for student in students:
    for c in random.sample(course_classes, k=3):
        Grade.objects.get_or_create(
            student=student,
            courseClass=c,
            defaults={
                'midterm': random.uniform(5.0, 8.0),
                'final': random.uniform(6.0, 9.0),
                'average': random.uniform(6.0, 9.0)
            }
        )
print(f"Đã tạo điểm cho sinh viên.")

# -------------------------------
# 9️⃣ Tạo thông báo (Notification)
# -------------------------------
notifications = []
for i in range(1, 6):
    notif, _ = Notification.objects.get_or_create(
        notificationId=f"N{i:03d}",
        defaults={
            'title': f'Thông báo số {i}',
            'content': f'Nội dung chi tiết của thông báo số {i}',
            'createdAt': datetime.now() - timedelta(days=random.randint(0, 7))
        }
    )
    notifications.append(notif)

for student in students:
    for notif in random.sample(notifications, k=random.randint(2, 4)):
        NotificationRecipient.objects.get_or_create(
            recipientId=f"{notif.notificationId}_{student.user.username}",
            defaults={
                'notification': notif,
                'user': student.user,
                'deliveryStatus': 'delivered',
                'deliveredAt': datetime.now() - timedelta(days=random.randint(0, 5)),
                'isRead': random.choice([True, False]),
                'readAt': None if random.random() < 0.5 else datetime.now()
            }
        )
print(f"Đã tạo thông báo & gắn cho sinh viên.")

print("Dữ liệu mẫu đã được tạo thành công!")
