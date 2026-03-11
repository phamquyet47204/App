import json

import boto3
from django.conf import settings
from django.core.mail import send_mail


def _value(obj, key, default=""):
    if isinstance(obj, dict):
        return obj.get(key, default)
    return getattr(obj, key, default)


def _full_name(user):
    if isinstance(user, dict):
        return f"{user.get('first_name', '')} {user.get('last_name', '')}".strip()
    if hasattr(user, "get_full_name"):
        return user.get_full_name()
    return ""


def _build_subject_and_message(user, course, action):
    subject = f"[{settings.EMAIL_SUBJECT_PREFIX}] {action} môn học thành công"
    message = (
        f"Xin chào {_full_name(user) or _value(user, 'username')},\n\n"
        f"Bạn đã {action.lower()} môn học thành công.\n"
        f"Mã môn: {_value(course, 'code')}\n"
        f"Tên môn: {_value(course, 'name')}\n\n"
        "Trân trọng."
    )
    return subject, message


def _send_via_lambda(to_email, subject, message):
    function_name = settings.EMAIL_LAMBDA_FUNCTION_NAME
    if not function_name:
        raise RuntimeError("EMAIL_LAMBDA_FUNCTION_NAME is required when EMAIL_PROVIDER=lambda")

    lambda_client = boto3.client("lambda", region_name=settings.EMAIL_LAMBDA_REGION)
    payload = {
        "to": to_email,
        "subject": subject,
        "text": message,
    }
    response = lambda_client.invoke(
        FunctionName=function_name,
        InvocationType="RequestResponse",
        Payload=json.dumps(payload).encode("utf-8"),
    )

    if response.get("FunctionError"):
        raw_error = response["Payload"].read().decode("utf-8", errors="ignore")
        raise RuntimeError(f"Lambda mail function failed: {raw_error}")

    raw_payload = response["Payload"].read().decode("utf-8", errors="ignore") or "{}"
    result = json.loads(raw_payload)
    if isinstance(result, dict) and int(result.get("statusCode", 200)) >= 400:
        raise RuntimeError(f"Lambda mail returned error: {raw_payload}")


def send_registration_email(user, course, action):
    subject, message = _build_subject_and_message(user, course, action)
    to_email = _value(user, "email")

    if settings.EMAIL_PROVIDER == "lambda":
        _send_via_lambda(to_email=to_email, subject=subject, message=message)
        return

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [to_email],
        fail_silently=False,
    )
