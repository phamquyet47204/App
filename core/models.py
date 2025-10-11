import json
import csv
from django.http import HttpResponse
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Permission
from django.conf import settings
from datetime import date
from django.contrib.auth import get_user_model

# Create your models here.
class User(AbstractUser):
    full_name = models.CharField(max_length=100, default='')
    phone = models.CharField(max_length=15, blank=True, null=True)
    
    USER_TYPE = [
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    ]
    user_type = models.CharField(max_length=10, choices=USER_TYPE, default='student')

    STATUS = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('suspended', 'Suspended'),
        ('graduated', 'Graduated'),
    ]
    status = models.CharField(max_length=10, choices=STATUS, default='active')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # AbstractUser đã có các trường: username, password, email, last_login, ...
    # => Không cần khai báo lại nữa.

    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"

User = get_user_model()

class Admin(models.Model):  
    user = models.OneToOneField('User', on_delete=models.CASCADE, primary_key=True)
    adminId = models.CharField(max_length=20, unique=True)
    adminCode = models.CharField(max_length=20, unique=True)
    permissions = models.ManyToManyField(Permission, blank=True)

    def __str__(self):
        return f"Admin {self.user.username} ({self.adminCode})"

class Student(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE, primary_key=True)
    studentId = models.CharField(max_length=20, unique=True)
    studentCode = models.CharField(max_length=20, unique=True)
    studentClass = models.ForeignKey('StudentClass', on_delete=models.SET_NULL, null=True, blank=True)
    dateOfBirth = models.DateField(null=True, blank=True)

    GENDER = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]
    gender = models.CharField(max_length=10, choices=GENDER, default='male')

    enrollmentYear = models.IntegerField()
    gpa = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    totalCredits = models.IntegerField(default=0)

    def __str__(self):
        return f"Student {self.user.username} ({self.studentCode})"

class Teacher(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE, primary_key=True)
    teacherId = models.CharField(max_length=20, unique=True)
    teacherCode = models.CharField(max_length=20, unique=True)
    department = models.ForeignKey('Department', on_delete=models.SET_NULL, null=True, blank=True)
    position = models.CharField(max_length=50)
    hireDate = models.DateField(default=date.today)

     # ========== CRUD METHODS ==========

    @classmethod
    def create_teacher(cls, user, teacherId, teacherCode, department=None, position='', hireDate=None):
        teacher = cls.objects.create(
            user=user,
            teacherId=teacherId,
            teacherCode=teacherCode,
            department=department,
            position=position,
            hireDate=hireDate
        )
        return teacher

    @classmethod
    def get_teacher(cls, teacherCode):
        #Lấy thông tin giáo viên theo mã code
        return cls.objects.filter(teacherCode=teacherCode).first()

    def update_teacher(self, **kwargs):
        #Cập nhật thông tin giáo viên
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.save()

    def delete_teacher(self):
        """Xóa giáo viên"""
        self.delete()

    # ========== METHODS ==========

    def viewAssignedClasses(self):
        #Xem danh sách các lớp được phân công
        return self.courseclass_set.all()  # giả định CourseClass có FK -> Teacher

    def inputGrades(self, courseClass, grades):
        """
        Nhập điểm cho lớp học
        - courseClass: đối tượng CourseClass
        - grades: danh sách Grade (chưa save)
        """
        for grade in grades:
            grade.save()

    def exportClassGrades(self, courseClass):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="grades_{courseClass.courseCode}.csv"'

        writer = csv.writer(response)
        writer.writerow(['Student', 'Subject', 'Grade', 'Semester'])

        grades = courseClass.grades.all()
        for g in grades:
            writer.writerow([
                g.student.user.username,
                g.subject.subjectName,
                getattr(g, 'score', 'N/A'),
                g.semester.name
            ])

        return response

    def updateStudentGrade(self, student, courseClass, newScore):
        from core.models import Grade  # tránh import vòng
        grade = Grade.objects.filter(student=student, courseClass=courseClass).first()
        if grade:
            grade.score = newScore
            grade.save()
            print(f"Updated grade for {student} in {courseClass} to {newScore}")
            return grade
        else:
            print("Grade record not found.")
            return None

    def __str__(self):
        return f"{self.user.username} - {self.teacherCode}"
    
class Department(models.Model):
    departmentId = models.CharField(max_length=20, primary_key=True)
    departmentCode = models.CharField(max_length=20, unique=True)
    departmentName = models.CharField(max_length=100)
    
    headTeacher = models.ForeignKey(
        'Teacher',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='headed_departments'
    )

    STATUS = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('suspended', 'Suspended'),
        ('graduated', 'Graduated'),
    ]
    status = models.CharField(max_length=10, choices=STATUS, default='active')

    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.departmentName

class Major(models.Model):
    majorId = models.CharField(max_length=20, primary_key=True)
    majorCode = models.CharField(max_length=20, unique=True)
    majorName = models.CharField(max_length=100)
    
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name='majors'
    )
    
    durationYears = models.IntegerField()
    totalCredits = models.IntegerField()
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.majorName
    
class StudentClass(models.Model):
    classId = models.CharField(max_length=20, primary_key=True)
    classCode = models.CharField(max_length=20, unique=True)
    className = models.CharField(max_length=100)

    major = models.ForeignKey(
        Major,
        on_delete=models.CASCADE,
        related_name='student_classes'
    )
    academicYear = models.CharField(max_length=20)

    advisorTeacher = models.ForeignKey(
        'Teacher',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='advisor_classes'
    )

    maxStudents = models.IntegerField()
    currentStudents = models.IntegerField(default=0)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.className

class Subject(models.Model):
    subjectId = models.CharField(max_length=20, primary_key=True)
    subjectCode = models.CharField(max_length=20, unique=True)
    subjectName = models.CharField(max_length=100)

    department = models.ForeignKey(
        'Department',
        on_delete=models.CASCADE,
        related_name='subjects'
    )

    credits = models.IntegerField()
    theoryHours = models.IntegerField()
    practiceHours = models.IntegerField()

    # Môn học tiên quyết (self-relation)
    prerequisites = models.ManyToManyField(
        'self',
        symmetrical=False,
        blank=True,
        related_name='required_for'
    )

    teachers = models.ManyToManyField(
        'Teacher',
        blank=True,
        related_name='subjects'
    )   

    STATUS = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('suspended', 'Suspended'),
        ('graduated', 'Graduated'),
    ]
    status = models.CharField(max_length=10, choices=STATUS, default='active')

    def __str__(self):
        return self.subjectName

class CourseClass(models.Model):
    courseClassId = models.CharField(max_length=20, primary_key=True)
    courseCode = models.CharField(max_length=20, unique=True)
    courseName = models.CharField(max_length=100)

    subject = models.ForeignKey(
        'Subject',
        on_delete=models.CASCADE,
        related_name='course_classes'
    )

    teacher = models.ForeignKey(
        'Teacher',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='course_classes'
    )

    semester = models.ForeignKey(
        'Semester',
        on_delete=models.CASCADE,
        related_name='course_classes'
    )
    room = models.CharField(max_length=50)
    schedule = models.DateTimeField(null=True, blank=True)

    maxStudents = models.IntegerField()
    currentStudents = models.IntegerField(default=0)

    status = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.courseName} ({self.courseCode})"

class CourseRegistration(models.Model):
    registrationId = models.CharField(max_length=20, primary_key=True)

    student = models.ForeignKey(
        'Student',
        on_delete=models.CASCADE,
        related_name='course_registrations'
    )

    courseClass = models.ForeignKey(
        'CourseClass',
        on_delete=models.CASCADE,
        related_name='course_registrations'
    )

    semester = models.ForeignKey(
        'Semester',
        on_delete=models.CASCADE,
        related_name='course_registrations'
    )

    registrationDate = models.DateField()

    REGISTRATION_STATUS = [
        ('registered', 'Registered'),
        ('dropped', 'Dropped'),
        ('completed', 'Completed'),
    ]

    status = models.CharField(
        max_length=20,
        choices=REGISTRATION_STATUS,
        default='registered'
    )

    def __str__(self):
        return f"{self.student.user.username} - {self.courseClass.courseName}"
   
class AcademicYear(models.Model):
    yearId = models.CharField(max_length=20, primary_key=True)  
    yearCode = models.CharField(max_length=20, unique=True)
    yearName = models.CharField(max_length=100)
    startDate = models.DateField()
    endDate = models.DateField()

    STATUS = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('suspended', 'Suspended'),
        ('graduated', 'Graduated'),
    ]
    status = models.CharField(max_length=10, choices=STATUS, default='active')

    def __str__(self):
        return self.yearName
    
class Semester(models.Model):
    semesterId = models.CharField(max_length=20, primary_key=True)
    semesterCode = models.CharField(max_length=20, unique=True)
    semesterName = models.CharField(max_length=100)

    academicYear = models.ForeignKey(
        'AcademicYear',
        on_delete=models.CASCADE,
        related_name='semesters'
    )

    startDate = models.DateField()
    endDate = models.DateField()
    registrationStart = models.DateTimeField()
    registrationEnd = models.DateTimeField()
  
    STATUS = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('suspended', 'Suspended'),
        ('graduated', 'Graduated'),
    ]
    status = models.CharField(max_length=10, choices=STATUS, default='active')

    def __str__(self):
        return self.semesterName

class Grade(models.Model):
    gradeId = models.CharField(max_length=20, primary_key=True)
    student = models.ForeignKey(
        'Student',
        on_delete=models.CASCADE,
        related_name='grades'
    )

    subject = models.ForeignKey(
        'Subject',
        on_delete=models.CASCADE,
        related_name='grades'
    )

    teacher = models.ForeignKey(
        'Teacher',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='grades'
    )

    courseClass = models.ForeignKey(
        'CourseClass',
        on_delete=models.CASCADE,
        related_name='grades'
    )

    semester = models.ForeignKey(
        'Semester',
        on_delete=models.CASCADE,
        related_name='grades'
    )

    assginmentscore = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    midterm_score = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    final_score = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    average_score = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)

    letterGrade = models.CharField(max_length=10)
    gradePoint = models.DecimalField(max_digits=3, decimal_places=1)
    isPassed = models.BooleanField()
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student.user.username} - {self.subject.subjectName}"

class TuitionFee(models.Model):
    tuitionFee = models.CharField(max_length=20, primary_key=True)

    student = models.ForeignKey(
        'Student',
        on_delete=models.CASCADE,
        related_name='tuition_fees'
    )

    semester = models.ForeignKey(
        'Semester',
        on_delete=models.CASCADE,
        related_name='tuition_fees'
    )

    totalCredit = models.IntegerField()
    feePerCredit = models.DecimalField(max_digits=10, decimal_places=3)
    totalAmount = models.DecimalField(max_digits=10, decimal_places=3)
    paidAmount = models.DecimalField(max_digits=10, decimal_places=3)

    PAYMENT_STATUS = [
        ('unpaid', 'Unpaid'),
        ('partial_paid', 'Partial Paid'),
        ('paid', 'Paid'),
    ]
    paymentStatus = models.CharField(max_length=12, choices=PAYMENT_STATUS, default='unpaid')
    dueDate = models.DateField()
    paymentDate = models.DateTimeField(null=True, blank=True)

    updatedBy = models.ForeignKey(
        'Admin',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='updated_tuitions'
    )

    notes = models.TextField(null=True, blank=True)
    def __str__(self):
        return f"{self.student.user.username} - {self.semester.semesterName}"
class DocumentType(models.Model):
    documentTypeId = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(null=True, blank=True)
    maxRequestsPerSemester = models.IntegerField()
    processingDays = models.IntegerField()

    STATUS = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('suspended', 'Suspended'),
        ('graduated', 'Graduated'),
    ]
    status = models.CharField(max_length=10, choices=STATUS, default='active')

    def __str__(self):
        return self.name
    
class DocumentRequest(models.Model):
    requestId = models.CharField(max_length=20, primary_key=True)

    student = models.ManyToManyField(
        'Student',
        related_name='document_requests'
    )

    documentType = models.ForeignKey(
        'DocumentType',
        on_delete=models.CASCADE,
        related_name='document_requests'
    )

    semester = models.ForeignKey(
        'Semester',
        on_delete=models.CASCADE,
        related_name='document_requests'
    )

    requestDate = models.DateTimeField()
    purpose = models.TextField()

    REQUEST_STATUS = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('completed', 'Completed'),
        ('rejected', 'Rejected'),
    ]
    status = models.CharField(max_length=10, choices=REQUEST_STATUS, default='pending')

    approvedBy = models.ForeignKey(
        'Admin',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_requests'
    )

    approvedDate = models.DateTimeField(null=True, blank=True)
    completedDate = models.DateTimeField(null=True, blank=True)
    rejectionReason = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.student.user.username} - {self.documentType.name}"

class Notification(models.Model):
    notificationId = models.CharField(max_length=20, primary_key=True)

    createdBy = models.ForeignKey(
        'User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_notifications'
    )

    title = models.CharField(max_length=100)
    content = models.TextField()

    TARGET_AUDIENCE = [
        ('all', 'All'),
        ('student', 'Students'),
        ('teacher', 'Teachers'),
        ('admin', 'Admins'),
        ('class', 'Class'),
        ('department', 'Department'),
    ]
    targetAudience = models.CharField(max_length=10, choices=TARGET_AUDIENCE, default='all')

    targetId = models.TextField(blank=True, default="[]")
    def get_target_ids(self):
        #Trả về danh sách ID dạng Python list
        return json.loads(self.targetId)

    def set_target_ids(self, ids):
        #Gán danh sách ID
        self.targetId = json.dumps(ids)
    
    NOTIFICATION_TYPE = [
        ('general', 'General'),
        ('academic', 'Academic'),
        ('administrative', 'Administrative'),
        ('urgent', 'Urgent'),
    ]
    notificationType = models.CharField(max_length=14, choices=NOTIFICATION_TYPE, default='general')

    priority = models.IntegerField()
    scheduledAt = models.DateTimeField(null=True, blank=True)

    STATUS = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('suspended', 'Suspended'),
        ('graduated', 'Graduated'),
    ]
    status = models.CharField(max_length=10, choices=STATUS, default='active')

    def __str__(self):
        return self.title
    
class NotificationRecipient(models.Model):
    recipientId = models.CharField(max_length=100, primary_key=True)
    notification = models.ForeignKey('Notification', on_delete=models.CASCADE, related_name='recipients')
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='notifications')
    
    DELIVERY_STATUS = [
        ('pending', 'Pending'),
        ('sent', 'Sent'),
        ('delivered', 'Delivered'),
        ('failed', 'Failed'),
    ]
    deliveryStatus = models.CharField(max_length=10, choices=DELIVERY_STATUS, default='pending')
    
    readAt = models.DateTimeField(null=True, blank=True)
    deliveredAt = models.DateTimeField(default=date.today)

    def __str__(self):
        return f"{self.user} - {self.notification} ({self.deliveryStatus})"

class PasswordResetToken(models.Model):
    token = models.CharField(max_length=100, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reset_tokens')
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)

    @classmethod
    def create_token(cls, user):
        import secrets
        from datetime import timedelta
        from django.utils import timezone
        
        token = secrets.token_urlsafe(32)
        expires_at = timezone.now() + timedelta(hours=24)
        return cls.objects.create(token=token, user=user, expires_at=expires_at)

    @classmethod
    def verify_token(cls, token):
        from django.utils import timezone
        try:
            reset_token = cls.objects.get(token=token, is_used=False)
            if reset_token.expires_at > timezone.now():
                return reset_token
        except cls.DoesNotExist:
            pass
        return None

    def __str__(self):
        return f"Reset token for {self.user.username}"