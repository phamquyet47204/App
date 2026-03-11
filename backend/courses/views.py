import multiprocessing
import threading
import time
from datetime import datetime, timedelta, timezone

from boto3.dynamodb.conditions import Key
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from dynamo import next_numeric_id, table, to_native

from .email_sender import send_registration_email
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


def _parse_iso_utc(value):
    if not value:
        return None
    if isinstance(value, datetime):
        return value
    text = str(value).replace("Z", "+00:00")
    try:
        return datetime.fromisoformat(text)
    except ValueError:
        return None


def _window_payload(item):
    item = to_native(item or {})
    now = datetime.now(timezone.utc)
    start_at = _parse_iso_utc(item.get("start_at"))
    end_at = _parse_iso_utc(item.get("end_at"))
    is_open = bool(item.get("is_open", False))

    can_register = is_open
    if start_at and now < start_at:
        can_register = False
    if end_at and now > end_at:
        can_register = False

    return {
        "id": int(item.get("id", 1)),
        "is_open": is_open,
        "start_at": item.get("start_at"),
        "end_at": item.get("end_at"),
        "updated_at": item.get("updated_at"),
        "can_register": can_register,
    }


def _get_registration_window_item():
    window_table = table("courses_registrationwindow")
    item = window_table.get_item(Key={"id": 1}).get("Item")
    if item:
        return item

    now_iso = datetime.now(timezone.utc).isoformat()
    default_item = {
        "id": 1,
        "is_open": False,
        "updated_at": now_iso,
    }
    window_table.put_item(Item=default_item)
    return default_item


class CourseListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        registration_rows = table("courses_registration").query(
            IndexName="student_course-index",
            KeyConditionExpression=Key("student_id").eq(int(request.user.id)),
        )
        registration_course_ids = {
            int(to_native(item["course_id"]))
            for item in registration_rows.get("Items", [])
        }

        courses = [to_native(item) for item in table("courses_course").scan().get("Items", [])]
        courses.sort(key=lambda c: c.get("code", ""))
        payload = []
        for course in courses:
            payload.append(
                {
                    "id": int(course["id"]),
                    "code": course.get("code", ""),
                    "name": course.get("name", ""),
                    "credits": int(course.get("credits", 0)),
                    "is_registered": int(course["id"]) in registration_course_ids,
                }
            )
        return Response(CourseSerializer(payload, many=True).data)


class RegistrationListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        reg_table = table("courses_registration")
        reg_rows = reg_table.query(
            IndexName="student_course-index",
            KeyConditionExpression=Key("student_id").eq(int(request.user.id)),
        ).get("Items", [])

        course_table = table("courses_course")
        payload = []
        for row in reg_rows:
            row = to_native(row)
            course_item = course_table.get_item(Key={"id": int(row["course_id"])}).get("Item")
            if not course_item:
                continue
            course = to_native(course_item)
            payload.append(
                {
                    "id": int(row["id"]),
                    "created_at": row.get("created_at", ""),
                    "course": {
                        "id": int(course["id"]),
                        "code": course.get("code", ""),
                        "name": course.get("name", ""),
                        "credits": int(course.get("credits", 0)),
                        "is_registered": True,
                    },
                }
            )
        payload.sort(key=lambda x: x.get("id", 0))
        return Response(RegistrationSerializer(payload, many=True).data)


class RegistrationActionView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, course_id):
        window_payload = _window_payload(_get_registration_window_item())
        if not window_payload["can_register"]:
            return Response(
                {"detail": "Hệ thống hiện không trong thời gian đăng ký môn."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        course_item = table("courses_course").get_item(Key={"id": int(course_id)}).get("Item")
        if not course_item:
            return Response({"detail": "Môn học không tồn tại."}, status=status.HTTP_404_NOT_FOUND)

        course = to_native(course_item)
        reg_table = table("courses_registration")
        existing = reg_table.query(
            IndexName="student_course-index",
            KeyConditionExpression=Key("student_id").eq(int(request.user.id)) & Key("course_id").eq(int(course_id)),
            Limit=1,
        )
        if existing.get("Items"):
            return Response(
                {"detail": "Bạn đã đăng ký môn học này rồi."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        registration_id = next_numeric_id("courses_registration")
        reg_table.put_item(
            Item={
                "id": registration_id,
                "student_id": int(request.user.id),
                "course_id": int(course_id),
                "created_at": datetime.now(timezone.utc).isoformat(),
            }
        )

        send_registration_email(request.user, course, "Đăng ký")
        return Response({"detail": "Đăng ký môn học thành công."}, status=status.HTTP_201_CREATED)

    def delete(self, request, course_id):
        window_payload = _window_payload(_get_registration_window_item())
        if not window_payload["can_register"]:
            return Response(
                {"detail": "Hệ thống hiện không trong thời gian đăng ký môn."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        course_item = table("courses_course").get_item(Key={"id": int(course_id)}).get("Item")
        if not course_item:
            return Response({"detail": "Môn học không tồn tại."}, status=status.HTTP_404_NOT_FOUND)

        course = to_native(course_item)
        reg_table = table("courses_registration")
        existing = reg_table.query(
            IndexName="student_course-index",
            KeyConditionExpression=Key("student_id").eq(int(request.user.id)) & Key("course_id").eq(int(course_id)),
            Limit=1,
        ).get("Items", [])
        if not existing:
            return Response(
                {"detail": "Bạn chưa đăng ký môn học này."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        reg_table.delete_item(Key={"id": int(to_native(existing[0]["id"]))})
        send_registration_email(request.user, course, "Hủy đăng ký")
        return Response({"detail": "Hủy đăng ký môn học thành công."}, status=status.HTTP_200_OK)


class RegistrationWindowView(APIView):
    authentication_classes = []
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        payload = _window_payload(_get_registration_window_item())
        return Response(RegistrationWindowSerializer(payload).data)


class AdminRegistrationWindowView(APIView):
    permission_classes = [IsStaffUser]

    def get(self, request):
        payload = _window_payload(_get_registration_window_item())
        return Response(RegistrationWindowSerializer(payload).data)

    def put(self, request):
        serializer = RegistrationWindowSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        current = to_native(_get_registration_window_item())
        for field in ("is_open", "start_at", "end_at"):
            if field in serializer.validated_data:
                current[field] = serializer.validated_data[field]
        current["updated_at"] = datetime.now(timezone.utc).isoformat()
        table("courses_registrationwindow").put_item(Item={"id": 1, **current})
        payload = _window_payload(current)
        return Response(RegistrationWindowSerializer(payload).data)


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
