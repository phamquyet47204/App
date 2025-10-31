from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import (
    User, Admin, Teacher, Student, Department, Major, StudentClass,
    Subject, CourseClass, CourseRegistration, AcademicYear, Semester,
    Grade, TuitionFee, DocumentType, DocumentRequest, Notification,
    NotificationRecipient, PasswordResetToken
)

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'full_name', 'user_type', 'status', 'last_login']
    list_filter = ['user_type', 'status', 'is_staff']
    search_fields = ['username', 'email', 'full_name']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('full_name', 'phone', 'user_type', 'status')
        }),
    )

@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    list_display = ['adminCode', 'user', 'adminId']
    search_fields = ['adminCode', 'user__username']

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['teacherCode', 'user', 'department', 'position', 'hireDate']
    list_filter = ['department', 'position']
    search_fields = ['teacherCode', 'user__username']

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['studentCode', 'user', 'studentClass', 'enrollmentYear', 'gpa']
    list_filter = ['studentClass', 'enrollmentYear', 'gender']
    search_fields = ['studentCode', 'user__username']

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['departmentCode', 'departmentName', 'headTeacher', 'status']
    list_filter = ['status']
    search_fields = ['departmentCode', 'departmentName']

@admin.register(Major)
class MajorAdmin(admin.ModelAdmin):
    list_display = ['majorCode', 'majorName', 'department', 'durationYears', 'totalCredits']
    list_filter = ['department']
    search_fields = ['majorCode', 'majorName']

@admin.register(StudentClass)
class StudentClassAdmin(admin.ModelAdmin):
    list_display = ['classCode', 'className', 'major', 'academicYear', 'currentStudents', 'maxStudents']
    list_filter = ['major', 'academicYear']
    search_fields = ['classCode', 'className']

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['subjectCode', 'subjectName', 'department', 'credits', 'status']
    list_filter = ['department', 'status']
    search_fields = ['subjectCode', 'subjectName']

@admin.register(CourseClass)
class CourseClassAdmin(admin.ModelAdmin):
    list_display = ['courseCode', 'courseName', 'subject', 'teacher', 'semester', 'currentStudents', 'maxStudents']
    list_filter = ['semester', 'subject']
    search_fields = ['courseCode', 'courseName']

@admin.register(CourseRegistration)
class CourseRegistrationAdmin(admin.ModelAdmin):
    list_display = ['registrationId', 'student', 'courseClass', 'semester', 'status', 'registrationDate']
    list_filter = ['status', 'semester']
    search_fields = ['student__user__username', 'courseClass__courseName']

@admin.register(AcademicYear)
class AcademicYearAdmin(admin.ModelAdmin):
    list_display = ['yearCode', 'yearName', 'startDate', 'endDate', 'status']
    list_filter = ['status']
    search_fields = ['yearCode', 'yearName']

@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ['semesterCode', 'semesterName', 'academicYear', 'startDate', 'endDate', 'status']
    list_filter = ['academicYear', 'status']
    search_fields = ['semesterCode', 'semesterName']

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ['gradeId', 'student', 'subject', 'courseClass', 'semester', 'letterGrade', 'isPassed']
    list_filter = ['semester', 'isPassed', 'letterGrade']
    search_fields = ['student__user__username', 'subject__subjectName']

@admin.register(TuitionFee)
class TuitionFeeAdmin(admin.ModelAdmin):
    list_display = ['tuitionFee', 'student', 'semester', 'totalAmount', 'paidAmount', 'paymentStatus']
    list_filter = ['paymentStatus', 'semester']
    search_fields = ['student__user__username']

@admin.register(DocumentType)
class DocumentTypeAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'maxRequestsPerSemester', 'processingDays', 'status']
    list_filter = ['status']
    search_fields = ['code', 'name']

@admin.register(DocumentRequest)
class DocumentRequestAdmin(admin.ModelAdmin):
    list_display = ['requestId', 'documentType', 'semester', 'status', 'requestDate']
    list_filter = ['status', 'semester']
    search_fields = ['requestId']

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['notificationId', 'title', 'targetAudience', 'notificationType', 'priority', 'status']
    list_filter = ['targetAudience', 'notificationType', 'status']
    search_fields = ['title', 'content']

@admin.register(NotificationRecipient)
class NotificationRecipientAdmin(admin.ModelAdmin):
    list_display = ['recipientId', 'notification', 'user', 'deliveryStatus', 'readAt']
    list_filter = ['deliveryStatus']
    search_fields = ['user__username', 'notification__title']

@admin.register(PasswordResetToken)
class PasswordResetTokenAdmin(admin.ModelAdmin):
    list_display = ['token', 'user', 'created_at', 'expires_at', 'is_used']
    list_filter = ['is_used', 'created_at']
    search_fields = ['user__username', 'token']
