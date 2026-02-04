from django.contrib import admin
from .models import Student, Course, Registration, RegistrationPeriod, AuditLog

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['mssv', 'full_name', 'email', 'department', 'is_active']
    search_fields = ['mssv', 'full_name', 'email']
    list_filter = ['is_active', 'department']

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'credits', 'semester', 'lecturer', 'is_active']
    search_fields = ['code', 'name']
    list_filter = ['semester', 'is_active']

@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'status', 'registered_at']
    search_fields = ['student__mssv', 'course__code']
    list_filter = ['status', 'registered_at']

@admin.register(RegistrationPeriod)
class RegistrationPeriodAdmin(admin.ModelAdmin):
    list_display = ['name', 'start_date', 'end_date', 'is_active']
    list_filter = ['is_active']

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ['student', 'action', 'course', 'created_at']
    list_filter = ['action', 'created_at']
    search_fields = ['student__mssv']
