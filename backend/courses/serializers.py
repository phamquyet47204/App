from rest_framework import serializers

from .models import Course, Registration, RegistrationWindow


class CourseSerializer(serializers.ModelSerializer):
    is_registered = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ["id", "code", "name", "credits", "is_registered"]

    def get_is_registered(self, obj):
        registration_course_ids = self.context.get("registration_course_ids", set())
        return obj.id in registration_course_ids


class RegistrationSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)

    class Meta:
        model = Registration
        fields = ["id", "course", "created_at"]


class RegistrationWindowSerializer(serializers.ModelSerializer):
    can_register = serializers.SerializerMethodField()

    class Meta:
        model = RegistrationWindow
        fields = ["is_open", "start_at", "end_at", "updated_at", "can_register"]

    def get_can_register(self, obj):
        return obj.can_register()
