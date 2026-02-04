import jwt
import os
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from datetime import datetime, timedelta
from .models import Student, Course, Registration, RegistrationPeriod

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'mssv', 'full_name', 'email', 'phone', 'department', 'is_admin']

class StudentRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['mssv', 'full_name', 'email', 'phone', 'department']

class LoginSerializer(serializers.Serializer):
    mssv = serializers.CharField(max_length=20)
    password = serializers.CharField(max_length=128, write_only=True)

    def validate(self, data):
        mssv = data.get('mssv')
        password = data.get('password')

        try:
            student = Student.objects.get(mssv=mssv)
        except Student.DoesNotExist:
            raise serializers.ValidationError("MSSV hoặc password không chính xác")

        if not student.check_password(password):
            raise serializers.ValidationError("MSSV hoặc password không chính xác")

        if not student.is_active:
            raise serializers.ValidationError("Tài khoản đã bị khóa")

        return {'student': student}

class CourseSerializer(serializers.ModelSerializer):
    enrolled_count = serializers.SerializerMethodField()
    available_spots = serializers.SerializerMethodField()
    is_registered = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = [
            'id', 'code', 'name', 'credits', 'semester',
            'capacity', 'lecturer', 'schedule', 'description',
            'is_active', 'enrolled_count', 'available_spots', 'is_registered'
        ]

    def get_enrolled_count(self, obj):
        return obj.get_enrolled_count()

    def get_available_spots(self, obj):
        return obj.get_available_spots()

    def get_is_registered(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Registration.objects.filter(
                student=request.user,
                course=obj,
                status='registered'
            ).exists()
        return False

class CourseCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['code', 'name', 'credits', 'semester', 'capacity', 'lecturer', 'schedule', 'description']

class RegistrationSerializer(serializers.ModelSerializer):
    course_info = CourseSerializer(source='course', read_only=True)
    
    class Meta:
        model = Registration
        fields = ['id', 'course', 'course_info', 'status', 'registered_at', 'cancelled_at']

class RegistrationCreateSerializer(serializers.Serializer):
    course_id = serializers.IntegerField()

    def validate_course_id(self, value):
        try:
            course = Course.objects.get(id=value, is_active=True)
        except Course.DoesNotExist:
            raise serializers.ValidationError("Môn học không tồn tại")
        return value

class RegistrationPeriodSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistrationPeriod
        fields = ['id', 'name', 'start_date', 'end_date', 'is_active']

class RegistrationPeriodUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistrationPeriod
        fields = ['name', 'start_date', 'end_date', 'is_active']

    def update(self, instance, validated_data):
        if validated_data.get('is_active'):
            # Đảm bảo chỉ có một kỳ đăng ký đang hoạt động
            RegistrationPeriod.objects.exclude(id=instance.id).update(is_active=False)
        
        return super().update(instance, validated_data)

class AdminLoginSerializer(serializers.Serializer):
    mssv = serializers.CharField(max_length=20)
    password = serializers.CharField(max_length=128, write_only=True)

    def validate(self, data):
        mssv = data.get('mssv')
        password = data.get('password')

        try:
            student = Student.objects.get(mssv=mssv, is_admin=True)
        except Student.DoesNotExist:
            raise serializers.ValidationError("Thông tin đăng nhập không chính xác")

        if not student.check_password(password):
            raise serializers.ValidationError("Thông tin đăng nhập không chính xác")

        return {'student': student}
