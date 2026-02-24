from django.conf import settings
from django.db import models
from django.utils import timezone


class Course(models.Model):
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=255)
    credits = models.PositiveIntegerField(default=3)

    def __str__(self):
        return f"{self.code} - {self.name}"


class RegistrationWindow(models.Model):
    is_open = models.BooleanField(default=False)
    start_at = models.DateTimeField(null=True, blank=True)
    end_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def can_register(self):
        if not self.is_open:
            return False

        now = timezone.now()
        if self.start_at and now < self.start_at:
            return False
        if self.end_at and now > self.end_at:
            return False
        return True

    @classmethod
    def get_solo(cls):
        window, _ = cls.objects.get_or_create(pk=1)
        return window


class Registration(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="registrations",
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="registrations")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("student", "course")

    def __str__(self):
        return f"{self.student.mssv} - {self.course.code}"
