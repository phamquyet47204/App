from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (("Student Info", {"fields": ("mssv",)}),)
    add_fieldsets = UserAdmin.add_fieldsets + (("Student Info", {"fields": ("mssv", "email")}),)
    list_display = ("username", "email", "mssv", "is_staff", "is_active")
    search_fields = ("username", "email", "mssv")
