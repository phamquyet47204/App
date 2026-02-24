from django.contrib import admin

from .models import Course, Registration, RegistrationWindow


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "credits")
    search_fields = ("code", "name")


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ("student", "course", "created_at")
    list_filter = ("course",)


@admin.register(RegistrationWindow)
class RegistrationWindowAdmin(admin.ModelAdmin):
    list_display = ("is_open", "start_at", "end_at", "updated_at")
