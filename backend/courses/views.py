from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .email_sender import send_registration_email
from .models import Course, Registration, RegistrationWindow
from .permissions import IsStaffUser
from .serializers import CourseSerializer, RegistrationSerializer, RegistrationWindowSerializer


class CourseListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        courses = Course.objects.all().order_by("code")
        registration_course_ids = set(
            Registration.objects.filter(student=request.user).values_list("course_id", flat=True)
        )
        serializer = CourseSerializer(
            courses,
            many=True,
            context={"registration_course_ids": registration_course_ids},
        )
        return Response(serializer.data)


class RegistrationListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        registrations = Registration.objects.filter(student=request.user).select_related("course")
        return Response(RegistrationSerializer(registrations, many=True).data)


class RegistrationActionView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, course_id):
        window = RegistrationWindow.get_solo()
        if not window.can_register():
            return Response(
                {"detail": "Hệ thống hiện không trong thời gian đăng ký môn."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        course = get_object_or_404(Course, pk=course_id)
        registration, created = Registration.objects.get_or_create(student=request.user, course=course)
        if not created:
            return Response(
                {"detail": "Bạn đã đăng ký môn học này rồi."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        send_registration_email(request.user, course, "Đăng ký")
        return Response({"detail": "Đăng ký môn học thành công."}, status=status.HTTP_201_CREATED)

    def delete(self, request, course_id):
        window = RegistrationWindow.get_solo()
        if not window.can_register():
            return Response(
                {"detail": "Hệ thống hiện không trong thời gian đăng ký môn."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        course = get_object_or_404(Course, pk=course_id)
        registration = Registration.objects.filter(student=request.user, course=course).first()
        if not registration:
            return Response(
                {"detail": "Bạn chưa đăng ký môn học này."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        registration.delete()
        send_registration_email(request.user, course, "Hủy đăng ký")
        return Response({"detail": "Hủy đăng ký môn học thành công."}, status=status.HTTP_200_OK)


class RegistrationWindowView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        window = RegistrationWindow.get_solo()
        return Response(RegistrationWindowSerializer(window).data)


class AdminRegistrationWindowView(APIView):
    permission_classes = [IsStaffUser]

    def get(self, request):
        window = RegistrationWindow.get_solo()
        return Response(RegistrationWindowSerializer(window).data)

    def put(self, request):
        window = RegistrationWindow.get_solo()
        serializer = RegistrationWindowSerializer(instance=window, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
