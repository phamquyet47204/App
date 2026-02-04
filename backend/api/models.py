from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import RegexValidator
from django.utils import timezone

class StudentManager(BaseUserManager):
    def create_user(self, mssv, password=None):
        if not mssv:
            raise ValueError('MSSV is required')
        user = self.model(mssv=mssv)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, mssv, password=None):
        user = self.create_user(mssv, password)
        user.is_admin = True
        user.save(using=self._db)
        return user

class Student(AbstractBaseUser):
    mssv = models.CharField(
        max_length=20,
        unique=True,
        validators=[RegexValidator(r'^[A-Z0-9]+$')],
        verbose_name='Mã số sinh viên'
    )
    full_name = models.CharField(max_length=200, verbose_name='Họ và tên')
    email = models.EmailField(unique=True, verbose_name='Email')
    phone = models.CharField(max_length=20, blank=True, verbose_name='Số điện thoại')
    department = models.CharField(max_length=100, verbose_name='Khoa')
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = StudentManager()

    USERNAME_FIELD = 'mssv'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'students'
        verbose_name = 'Sinh viên'
        verbose_name_plural = 'Sinh viên'

    def __str__(self):
        return f"{self.mssv} - {self.full_name}"

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

    @property
    def is_staff(self):
        return self.is_admin

class Course(models.Model):
    code = models.CharField(max_length=50, unique=True, verbose_name='Mã môn học')
    name = models.CharField(max_length=200, verbose_name='Tên môn học')
    credits = models.IntegerField(verbose_name='Số tín chỉ')
    semester = models.IntegerField(verbose_name='Kỳ học')
    capacity = models.IntegerField(verbose_name='Sức chứa')
    lecturer = models.CharField(max_length=100, verbose_name='Giáo viên')
    schedule = models.TextField(verbose_name='Lịch học')
    description = models.TextField(blank=True, verbose_name='Mô tả')
    is_active = models.BooleanField(default=True, verbose_name='Kích hoạt')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'courses'
        verbose_name = 'Môn học'
        verbose_name_plural = 'Môn học'

    def __str__(self):
        return f"{self.code} - {self.name}"

    def get_enrolled_count(self):
        return self.registrations.filter(status='registered').count()

    def get_available_spots(self):
        return self.capacity - self.get_enrolled_count()

class Registration(models.Model):
    STATUS_CHOICES = [
        ('registered', 'Đã đăng ký'),
        ('cancelled', 'Đã huỷ'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='registrations')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='registrations')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='registered')
    registered_at = models.DateTimeField(auto_now_add=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'registrations'
        unique_together = ('student', 'course')
        verbose_name = 'Đăng ký môn học'
        verbose_name_plural = 'Đăng ký môn học'

    def __str__(self):
        return f"{self.student.mssv} - {self.course.code}"

class RegistrationPeriod(models.Model):
    name = models.CharField(max_length=200, verbose_name='Tên kỳ đăng ký')
    start_date = models.DateTimeField(verbose_name='Ngày bắt đầu')
    end_date = models.DateTimeField(verbose_name='Ngày kết thúc')
    is_active = models.BooleanField(default=False, verbose_name='Đang kích hoạt')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'registration_periods'
        verbose_name = 'Kỳ đăng ký'
        verbose_name_plural = 'Kỳ đăng ký'

    def __str__(self):
        return self.name

    @classmethod
    def is_registration_open(cls):
        now = timezone.now()
        period = cls.objects.filter(
            is_active=True,
            start_date__lte=now,
            end_date__gte=now
        ).first()
        return period is not None

    @classmethod
    def get_active_period(cls):
        return cls.objects.filter(is_active=True).first()

class AuditLog(models.Model):
    ACTION_CHOICES = [
        ('register', 'Đăng ký'),
        ('cancel', 'Huỷ đăng ký'),
        ('login', 'Đăng nhập'),
        ('logout', 'Đăng xuất'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='audit_logs')
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True)
    details = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'audit_logs'
        verbose_name = 'Nhật ký hoạt động'
        verbose_name_plural = 'Nhật ký hoạt động'

    def __str__(self):
        return f"{self.student.mssv} - {self.action}"
