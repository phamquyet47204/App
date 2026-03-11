from rest_framework import serializers

class CourseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    code = serializers.CharField()
    name = serializers.CharField()
    credits = serializers.IntegerField()
    is_registered = serializers.BooleanField()


class RegistrationSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    course = CourseSerializer()
    created_at = serializers.CharField()


class RegistrationWindowSerializer(serializers.Serializer):
    is_open = serializers.BooleanField(required=False)
    start_at = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    end_at = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    updated_at = serializers.CharField(required=False)
    can_register = serializers.BooleanField(required=False)
