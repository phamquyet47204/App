import multiprocessing
import threading
import time
from datetime import datetime, timedelta, timezone

from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .email_sender import send_registration_email
from .models import Course, Registration, RegistrationWindow
from .permissions import IsStaffUser
from .serializers import CourseSerializer, RegistrationSerializer, RegistrationWindowSerializer


CPU_STRESS_PERCENT = 80
CPU_STRESS_DURATION_SECONDS = 120
_stress_lock = threading.Lock()
_stress_running_until = None
_stress_last_started_at = None
_stress_last_finished_at = None


def _cpu_stress_worker(stop_at, cpu_percent):
    period = 0.1
    busy_time = period * max(0, min(cpu_percent, 100)) / 100.0

    while time.time() < stop_at:
        busy_until = time.perf_counter() + busy_time
        while time.perf_counter() < busy_until:
            pass

        sleep_time = period - busy_time
        if sleep_time > 0:
            time.sleep(sleep_time)


def _run_cpu_stress(duration_seconds, cpu_percent):
    global _stress_running_until, _stress_last_started_at, _stress_last_finished_at

    stop_at = time.time() + duration_seconds
    process_count = max(1, multiprocessing.cpu_count())
    workers = []

    with _stress_lock:
        _stress_last_started_at = datetime.now(timezone.utc)
        _stress_running_until = datetime.now(timezone.utc) + timedelta(seconds=duration_seconds)

    try:
        for _ in range(process_count):
            process = multiprocessing.Process(target=_cpu_stress_worker, args=(stop_at, cpu_percent))
            process.start()
            workers.append(process)

        for process in workers:
            process.join(timeout=max(1, duration_seconds + 5))
            if process.is_alive():
                process.terminate()
                process.join(timeout=2)
    finally:
        with _stress_lock:
            _stress_running_until = None
            _stress_last_finished_at = datetime.now(timezone.utc)


def _get_stress_status():
    with _stress_lock:
        now = datetime.now(timezone.utc)
        running = _stress_running_until is not None and _stress_running_until > now
        remaining_seconds = 0
        if running:
            remaining_seconds = int((_stress_running_until - now).total_seconds())

        return {
            "running": running,
            "target_cpu_percent": CPU_STRESS_PERCENT,
            "duration_seconds": CPU_STRESS_DURATION_SECONDS,
            "remaining_seconds": max(0, remaining_seconds),
            "last_started_at": _stress_last_started_at.isoformat() if _stress_last_started_at else None,
            "last_finished_at": _stress_last_finished_at.isoformat() if _stress_last_finished_at else None,
        }


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
    authentication_classes = []
    permission_classes = [permissions.AllowAny]

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


class AdminCpuStressTestView(APIView):
    permission_classes = [IsStaffUser]

    def get(self, request):
        return Response(_get_stress_status())

    def post(self, request):
        current_status = _get_stress_status()
        if current_status["running"]:
            return Response(
                {"detail": "Stress test đang chạy.", **current_status},
                status=status.HTTP_409_CONFLICT,
            )

        thread = threading.Thread(
            target=_run_cpu_stress,
            args=(CPU_STRESS_DURATION_SECONDS, CPU_STRESS_PERCENT),
            daemon=True,
        )
        thread.start()

        return Response(
            {
                "detail": "Đã bắt đầu stress test CPU 80% trong 2 phút.",
                **_get_stress_status(),
            },
            status=status.HTTP_202_ACCEPTED,
        )


class HealthCheckView(APIView):
    authentication_classes = []
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        return Response({"status": "ok"}, status=status.HTTP_200_OK)
