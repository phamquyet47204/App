"""
DynamoDB Export Script
Xuất tất cả dữ liệu từ DynamoDB ra file JSON và CSV (cho bảng users).

Cách chạy:
  python dynamodb_export.py                    # xuất tất cả bảng
  python dynamodb_export.py accounts_user      # xuất một bảng cụ thể

Output:
  exports/
    accounts_user.json
    accounts_user.csv          (chỉ bảng accounts_user)
    authtoken_token.json
    courses_course.json
    courses_registration.json
    courses_registrationwindow.json
    auth_permission.json
    auth_group.json
    auth_group_permissions.json
    accounts_user_groups.json
    accounts_user_user_permissions.json
    django_content_type.json
    django_migrations.json
    django_admin_log.json
    django_session.json
"""

import boto3
import json
import csv
import os
import sys
from decimal import Decimal
from datetime import datetime
from boto3.dynamodb.conditions import Key

# ─────────────────────────────────────────────
# Cấu hình — giống dynamodb_setup.py
# ─────────────────────────────────────────────
REGION = "ap-southeast-1"
USE_LOCAL = False
LOCAL_ENDPOINT = "http://localhost:8000"
TABLE_PREFIX = ""
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "exports")

ALL_TABLES = [
    "accounts_user",
    "accounts_user_groups",
    "accounts_user_user_permissions",
    "auth_group",
    "auth_group_permissions",
    "auth_permission",
    "authtoken_token",
    "courses_course",
    "courses_registration",
    "courses_registrationwindow",
    "django_admin_log",
    "django_content_type",
    "django_migrations",
    "django_session",
]


def get_dynamodb_resource():
    if USE_LOCAL:
        return boto3.resource(
            "dynamodb",
            region_name="us-east-1",
            endpoint_url=LOCAL_ENDPOINT,
            aws_access_key_id="dummy",
            aws_secret_access_key="dummy",
        )
    return boto3.resource("dynamodb", region_name=REGION)


def tbl(name):
    return f"{TABLE_PREFIX}{name}"


# ─────────────────────────────────────────────
# Scan toàn bộ bảng (xử lý phân trang)
# ─────────────────────────────────────────────

def scan_all(table):
    items = []
    resp = table.scan()
    items.extend(resp.get("Items", []))
    while "LastEvaluatedKey" in resp:
        resp = table.scan(ExclusiveStartKey=resp["LastEvaluatedKey"])
        items.extend(resp.get("Items", []))
    return items


# ─────────────────────────────────────────────
# Chuyển đổi kiểu dữ liệu Decimal → int/float
# ─────────────────────────────────────────────

def default_serializer(obj):
    if isinstance(obj, Decimal):
        return int(obj) if obj % 1 == 0 else float(obj)
    raise TypeError(f"Type {type(obj)} not serializable")


def convert(obj):
    """Đệ quy chuyển Decimal → int/float để serialize JSON."""
    if isinstance(obj, list):
        return [convert(i) for i in obj]
    if isinstance(obj, dict):
        return {k: convert(v) for k, v in obj.items()}
    if isinstance(obj, Decimal):
        return int(obj) if obj % 1 == 0 else float(obj)
    return obj


# ─────────────────────────────────────────────
# Xuất JSON
# ─────────────────────────────────────────────

def export_json(table_name, items):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    path = os.path.join(OUTPUT_DIR, f"{table_name}.json")
    data = convert(items)
    # Sắp xếp theo id nếu có
    try:
        data.sort(key=lambda x: x.get("id", x.get("key", x.get("session_key", 0))))
    except TypeError:
        pass
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return path


# ─────────────────────────────────────────────
# Xuất CSV (dành cho accounts_user)
# ─────────────────────────────────────────────

USER_CSV_FIELDS = [
    "id", "username", "mssv", "email",
    "is_staff", "is_superuser", "is_active",
    "date_joined", "last_login",
]

def export_users_csv(items):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    path = os.path.join(OUTPUT_DIR, f"users_export_{timestamp}.csv")
    data = sorted(convert(items), key=lambda x: x.get("id", 0))
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=USER_CSV_FIELDS, extrasaction="ignore")
        writer.writeheader()
        for row in data:
            # Chuẩn hóa boolean thành 0/1 giống MySQL dump gốc
            row["is_staff"]       = 1 if row.get("is_staff") else 0
            row["is_superuser"]   = 1 if row.get("is_superuser") else 0
            row["is_active"]      = 1 if row.get("is_active") else 0
            row["last_login"]     = row.get("last_login", "NULL") or "NULL"
            writer.writerow(row)
    return path


# ─────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────


def upload_to_s3(local_path, bucket, prefix="dynamodb-exports"):
    s3 = boto3.client("s3", region_name=REGION)
    filename = os.path.basename(local_path)
    key = f"{prefix}/{filename}"
    s3.upload_file(local_path, bucket, key)
    return f"s3://{bucket}/{key}"


def main():
    # Lấy S3 bucket từ arg hoặc env (optional)
    # Dùng: python dynamodb_export.py [table1 table2 ...] --s3 <bucket-name>
    args = sys.argv[1:]
    s3_bucket = None
    if "--s3" in args:
        idx = args.index("--s3")
        s3_bucket = args[idx + 1]
        args = args[:idx] + args[idx + 2:]

    target_tables = args if args else ALL_TABLES

    db = get_dynamodb_resource()
    print(f"\n=== Xuất dữ liệu DynamoDB → {OUTPUT_DIR}/ ===\n")
    exported_files = []
    for name in target_tables:
        full_name = tbl(name)
        try:
            table = db.Table(full_name)
            items = scan_all(table)
            json_path = export_json(name, items)
            exported_files.append(json_path)
            print(f"  [OK] {full_name:45s} → {os.path.relpath(json_path)} ({len(items)} items)")

            if name == "accounts_user" and items:
                csv_path = export_users_csv(items)
                exported_files.append(csv_path)
                print(f"       {'':45s}   {os.path.relpath(csv_path)} (CSV)")

        except Exception as e:
            print(f"  [ERR] {full_name}: {e}")

    print(f"\n✓ Hoàn tất local! Kiểm tra thư mục: {OUTPUT_DIR}/\n")

    if s3_bucket:
        print(f"=== Upload lên s3://{s3_bucket}/dynamodb-exports/ ===\n")
        for f in exported_files:
            try:
                s3_uri = upload_to_s3(f, s3_bucket)
                print(f"  [S3] {os.path.basename(f):50s} → {s3_uri}")
            except Exception as e:
                print(f"  [S3 ERR] {os.path.basename(f)}: {e}")
        print(f"\n✓ Upload hoàn tất!\n")


if __name__ == "__main__":
    main()
