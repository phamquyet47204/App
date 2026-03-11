"""
DynamoDB Setup Script - thay thế cho sql.sql (MySQL)
Database: course_registration
Chạy: python dynamodb_setup.py

Yêu cầu:
  pip install boto3
  AWS credentials phải được cấu hình (~/.aws/credentials hoặc biến môi trường)

Để dùng DynamoDB Local (local dev):
  docker run -p 8000:8000 amazon/dynamodb-local
  Đặt USE_LOCAL=True bên dưới
"""

import boto3
from botocore.exceptions import ClientError
from decimal import Decimal

# ─────────────────────────────────────────────
# Cấu hình
# ─────────────────────────────────────────────
REGION = "ap-southeast-1"          # Singapore
USE_LOCAL = False                   # True → dùng DynamoDB Local (localhost:8000)
LOCAL_ENDPOINT = "http://localhost:8000"
TABLE_PREFIX = ""                   # Tiền tố bảng, vd: "prod_" hoặc để trống

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
    """Trả về tên bảng có prefix."""
    return f"{TABLE_PREFIX}{name}"


# ─────────────────────────────────────────────
# Tạo bảng
# ─────────────────────────────────────────────

TABLE_DEFINITIONS = [
    # ── accounts_user ──────────────────────────────────────────────────────
    {
        "TableName": tbl("accounts_user"),
        "KeySchema": [
            {"AttributeName": "id", "KeyType": "HASH"},
        ],
        "AttributeDefinitions": [
            {"AttributeName": "id",       "AttributeType": "N"},
            {"AttributeName": "username", "AttributeType": "S"},
            {"AttributeName": "mssv",     "AttributeType": "S"},
            {"AttributeName": "email",    "AttributeType": "S"},
        ],
        "GlobalSecondaryIndexes": [
            {
                "IndexName": "username-index",
                "KeySchema": [{"AttributeName": "username", "KeyType": "HASH"}],
                "Projection": {"ProjectionType": "ALL"},
            },
            {
                "IndexName": "mssv-index",
                "KeySchema": [{"AttributeName": "mssv", "KeyType": "HASH"}],
                "Projection": {"ProjectionType": "ALL"},
            },
            {
                "IndexName": "email-index",
                "KeySchema": [{"AttributeName": "email", "KeyType": "HASH"}],
                "Projection": {"ProjectionType": "ALL"},
            },
        ],
        "BillingMode": "PAY_PER_REQUEST",
    },

    # ── accounts_user_groups ───────────────────────────────────────────────
    {
        "TableName": tbl("accounts_user_groups"),
        "KeySchema": [
            {"AttributeName": "id", "KeyType": "HASH"},
        ],
        "AttributeDefinitions": [
            {"AttributeName": "id",      "AttributeType": "N"},
            {"AttributeName": "user_id", "AttributeType": "N"},
        ],
        "GlobalSecondaryIndexes": [
            {
                "IndexName": "user_id-index",
                "KeySchema": [{"AttributeName": "user_id", "KeyType": "HASH"}],
                "Projection": {"ProjectionType": "ALL"},
            },
        ],
        "BillingMode": "PAY_PER_REQUEST",
    },

    # ── accounts_user_user_permissions ────────────────────────────────────
    {
        "TableName": tbl("accounts_user_user_permissions"),
        "KeySchema": [
            {"AttributeName": "id", "KeyType": "HASH"},
        ],
        "AttributeDefinitions": [
            {"AttributeName": "id",      "AttributeType": "N"},
            {"AttributeName": "user_id", "AttributeType": "N"},
        ],
        "GlobalSecondaryIndexes": [
            {
                "IndexName": "user_id-index",
                "KeySchema": [{"AttributeName": "user_id", "KeyType": "HASH"}],
                "Projection": {"ProjectionType": "ALL"},
            },
        ],
        "BillingMode": "PAY_PER_REQUEST",
    },

    # ── auth_group ────────────────────────────────────────────────────────
    {
        "TableName": tbl("auth_group"),
        "KeySchema": [
            {"AttributeName": "id", "KeyType": "HASH"},
        ],
        "AttributeDefinitions": [
            {"AttributeName": "id",   "AttributeType": "N"},
            {"AttributeName": "name", "AttributeType": "S"},
        ],
        "GlobalSecondaryIndexes": [
            {
                "IndexName": "name-index",
                "KeySchema": [{"AttributeName": "name", "KeyType": "HASH"}],
                "Projection": {"ProjectionType": "ALL"},
            },
        ],
        "BillingMode": "PAY_PER_REQUEST",
    },

    # ── auth_group_permissions ────────────────────────────────────────────
    {
        "TableName": tbl("auth_group_permissions"),
        "KeySchema": [
            {"AttributeName": "id", "KeyType": "HASH"},
        ],
        "AttributeDefinitions": [
            {"AttributeName": "id",       "AttributeType": "N"},
            {"AttributeName": "group_id", "AttributeType": "N"},
        ],
        "GlobalSecondaryIndexes": [
            {
                "IndexName": "group_id-index",
                "KeySchema": [{"AttributeName": "group_id", "KeyType": "HASH"}],
                "Projection": {"ProjectionType": "ALL"},
            },
        ],
        "BillingMode": "PAY_PER_REQUEST",
    },

    # ── auth_permission ───────────────────────────────────────────────────
    {
        "TableName": tbl("auth_permission"),
        "KeySchema": [
            {"AttributeName": "id", "KeyType": "HASH"},
        ],
        "AttributeDefinitions": [
            {"AttributeName": "id",              "AttributeType": "N"},
            {"AttributeName": "content_type_id", "AttributeType": "N"},
            {"AttributeName": "codename",        "AttributeType": "S"},
        ],
        "GlobalSecondaryIndexes": [
            {
                "IndexName": "content_type_codename-index",
                "KeySchema": [
                    {"AttributeName": "content_type_id", "KeyType": "HASH"},
                    {"AttributeName": "codename",        "KeyType": "RANGE"},
                ],
                "Projection": {"ProjectionType": "ALL"},
            },
        ],
        "BillingMode": "PAY_PER_REQUEST",
    },

    # ── authtoken_token ───────────────────────────────────────────────────
    {
        "TableName": tbl("authtoken_token"),
        "KeySchema": [
            {"AttributeName": "key", "KeyType": "HASH"},
        ],
        "AttributeDefinitions": [
            {"AttributeName": "key",     "AttributeType": "S"},
            {"AttributeName": "user_id", "AttributeType": "N"},
        ],
        "GlobalSecondaryIndexes": [
            {
                "IndexName": "user_id-index",
                "KeySchema": [{"AttributeName": "user_id", "KeyType": "HASH"}],
                "Projection": {"ProjectionType": "ALL"},
            },
        ],
        "BillingMode": "PAY_PER_REQUEST",
    },

    # ── courses_course ────────────────────────────────────────────────────
    {
        "TableName": tbl("courses_course"),
        "KeySchema": [
            {"AttributeName": "id", "KeyType": "HASH"},
        ],
        "AttributeDefinitions": [
            {"AttributeName": "id",   "AttributeType": "N"},
            {"AttributeName": "code", "AttributeType": "S"},
        ],
        "GlobalSecondaryIndexes": [
            {
                "IndexName": "code-index",
                "KeySchema": [{"AttributeName": "code", "KeyType": "HASH"}],
                "Projection": {"ProjectionType": "ALL"},
            },
        ],
        "BillingMode": "PAY_PER_REQUEST",
    },

    # ── courses_registration ──────────────────────────────────────────────
    {
        "TableName": tbl("courses_registration"),
        "KeySchema": [
            {"AttributeName": "id", "KeyType": "HASH"},
        ],
        "AttributeDefinitions": [
            {"AttributeName": "id",         "AttributeType": "N"},
            {"AttributeName": "student_id", "AttributeType": "N"},
            {"AttributeName": "course_id",  "AttributeType": "N"},
        ],
        "GlobalSecondaryIndexes": [
            {
                "IndexName": "student_course-index",
                "KeySchema": [
                    {"AttributeName": "student_id", "KeyType": "HASH"},
                    {"AttributeName": "course_id",  "KeyType": "RANGE"},
                ],
                "Projection": {"ProjectionType": "ALL"},
            },
        ],
        "BillingMode": "PAY_PER_REQUEST",
    },

    # ── courses_registrationwindow ────────────────────────────────────────
    {
        "TableName": tbl("courses_registrationwindow"),
        "KeySchema": [
            {"AttributeName": "id", "KeyType": "HASH"},
        ],
        "AttributeDefinitions": [
            {"AttributeName": "id", "AttributeType": "N"},
        ],
        "BillingMode": "PAY_PER_REQUEST",
    },

    # ── django_admin_log ──────────────────────────────────────────────────
    {
        "TableName": tbl("django_admin_log"),
        "KeySchema": [
            {"AttributeName": "id", "KeyType": "HASH"},
        ],
        "AttributeDefinitions": [
            {"AttributeName": "id",      "AttributeType": "N"},
            {"AttributeName": "user_id", "AttributeType": "N"},
        ],
        "GlobalSecondaryIndexes": [
            {
                "IndexName": "user_id-index",
                "KeySchema": [{"AttributeName": "user_id", "KeyType": "HASH"}],
                "Projection": {"ProjectionType": "ALL"},
            },
        ],
        "BillingMode": "PAY_PER_REQUEST",
    },

    # ── django_content_type ───────────────────────────────────────────────
    {
        "TableName": tbl("django_content_type"),
        "KeySchema": [
            {"AttributeName": "id", "KeyType": "HASH"},
        ],
        "AttributeDefinitions": [
            {"AttributeName": "id",        "AttributeType": "N"},
            {"AttributeName": "app_label", "AttributeType": "S"},
            {"AttributeName": "model",     "AttributeType": "S"},
        ],
        "GlobalSecondaryIndexes": [
            {
                "IndexName": "app_label_model-index",
                "KeySchema": [
                    {"AttributeName": "app_label", "KeyType": "HASH"},
                    {"AttributeName": "model",     "KeyType": "RANGE"},
                ],
                "Projection": {"ProjectionType": "ALL"},
            },
        ],
        "BillingMode": "PAY_PER_REQUEST",
    },

    # ── django_migrations ─────────────────────────────────────────────────
    {
        "TableName": tbl("django_migrations"),
        "KeySchema": [
            {"AttributeName": "id", "KeyType": "HASH"},
        ],
        "AttributeDefinitions": [
            {"AttributeName": "id", "AttributeType": "N"},
        ],
        "BillingMode": "PAY_PER_REQUEST",
    },

    # ── django_session ────────────────────────────────────────────────────
    {
        "TableName": tbl("django_session"),
        "KeySchema": [
            {"AttributeName": "session_key", "KeyType": "HASH"},
        ],
        "AttributeDefinitions": [
            {"AttributeName": "session_key", "AttributeType": "S"},
            {"AttributeName": "expire_date", "AttributeType": "S"},
        ],
        "GlobalSecondaryIndexes": [
            {
                "IndexName": "expire_date-index",
                "KeySchema": [{"AttributeName": "expire_date", "KeyType": "HASH"}],
                "Projection": {"ProjectionType": "ALL"},
            },
        ],
        "BillingMode": "PAY_PER_REQUEST",
    },
]


def create_tables(db):
    for definition in TABLE_DEFINITIONS:
        table_name = definition["TableName"]
        try:
            table = db.create_table(**definition)
            table.wait_until_exists()
            print(f"  [OK] Tạo bảng: {table_name}")
        except ClientError as e:
            if e.response["Error"]["Code"] == "ResourceInUseException":
                print(f"  [--] Bảng đã tồn tại: {table_name}")
            else:
                raise


# ─────────────────────────────────────────────
# Seed dữ liệu
# ─────────────────────────────────────────────

def seed_accounts_user(db):
    table = db.Table(tbl("accounts_user"))
    items = [
        {
            "id":           Decimal(1),
            "password":     "pbkdf2_sha256$870000$jqylm1CA0GlbfeJCefcOoG$FPWqO+6vLsQcE+BcauINzFSoMiDbcVjWPF7KpaptaHY=",
            "last_login":   None,
            "is_superuser": False,
            "username":     "sv001",
            "first_name":   "An",
            "last_name":    "Nguyen",
            "is_staff":     False,
            "is_active":    True,
            "date_joined":  "2026-02-24T00:00:00.000000",
            "mssv":         "20123456",
            "email":        "phamquyet472k4@gmail.com",
        },
        {
            "id":           Decimal(2),
            "password":     "pbkdf2_sha256$870000$9KzroofR7Ie1fCS32t07f5$odEy1ettJarFKSIRX0sUzWRFj2Iurb70bCRoRYO3uWw=",
            "last_login":   None,
            "is_superuser": True,
            "username":     "admin",
            "first_name":   "Admin",
            "last_name":    "User",
            "is_staff":     True,
            "is_active":    True,
            "date_joined":  "2026-02-24T00:00:00.000000",
            "mssv":         "00000000",
            "email":        "enormitpham@gmail.com",
        },
    ]
    for item in items:
        # Loại bỏ None values (DynamoDB không chấp nhận null trong put_item)
        clean = {k: v for k, v in item.items() if v is not None}
        table.put_item(Item=clean)
    print(f"  [OK] Seed accounts_user ({len(items)} items)")


def seed_authtoken_token(db):
    table = db.Table(tbl("authtoken_token"))
    table.put_item(Item={
        "key":     "454917f13b31bc4ee57684d85c9fb9735535c575",
        "created": "2026-02-24T06:39:53.766254",
        "user_id": Decimal(1),
    })
    print("  [OK] Seed authtoken_token (1 item)")


def seed_courses_course(db):
    table = db.Table(tbl("courses_course"))
    items = [
        {"id": Decimal(1), "code": "MATH101", "name": "Giai tich 1",         "credits": Decimal(3)},
        {"id": Decimal(2), "code": "PHYS101", "name": "Vat ly dai cuong",    "credits": Decimal(3)},
        {"id": Decimal(3), "code": "CS101",   "name": "Nhap mon lap trinh",  "credits": Decimal(4)},
        {"id": Decimal(4), "code": "CS102",   "name": "Cau truc du lieu",    "credits": Decimal(4)},
        {"id": Decimal(5), "code": "ENG101",  "name": "Tieng Anh 1",         "credits": Decimal(2)},
    ]
    for item in items:
        table.put_item(Item=item)
    print(f"  [OK] Seed courses_course ({len(items)} items)")


def seed_courses_registration(db):
    table = db.Table(tbl("courses_registration"))
    items = [
        {"id": Decimal(5), "created_at": "2026-02-24T06:35:13.792375", "course_id": Decimal(4), "student_id": Decimal(2)},
        {"id": Decimal(6), "created_at": "2026-02-24T06:39:54.961458", "course_id": Decimal(3), "student_id": Decimal(1)},
    ]
    for item in items:
        table.put_item(Item=item)
    print(f"  [OK] Seed courses_registration ({len(items)} items)")


def seed_courses_registrationwindow(db):
    table = db.Table(tbl("courses_registrationwindow"))
    table.put_item(Item={
        "id":         Decimal(1),
        "is_open":    True,
        "updated_at": "2026-02-24T06:22:57.880535",
        # start_at / end_at là NULL nên bỏ qua
    })
    print("  [OK] Seed courses_registrationwindow (1 item)")


def seed_auth_permission(db):
    table = db.Table(tbl("auth_permission"))
    permissions = [
        (1,'Can add log entry',1,'add_logentry'),
        (2,'Can change log entry',1,'change_logentry'),
        (3,'Can delete log entry',1,'delete_logentry'),
        (4,'Can view log entry',1,'view_logentry'),
        (5,'Can add permission',2,'add_permission'),
        (6,'Can change permission',2,'change_permission'),
        (7,'Can delete permission',2,'delete_permission'),
        (8,'Can view permission',2,'view_permission'),
        (9,'Can add group',3,'add_group'),
        (10,'Can change group',3,'change_group'),
        (11,'Can delete group',3,'delete_group'),
        (12,'Can view group',3,'view_group'),
        (13,'Can add content type',4,'add_contenttype'),
        (14,'Can change content type',4,'change_contenttype'),
        (15,'Can delete content type',4,'delete_contenttype'),
        (16,'Can view content type',4,'view_contenttype'),
        (17,'Can add session',5,'add_session'),
        (18,'Can change session',5,'change_session'),
        (19,'Can delete session',5,'delete_session'),
        (20,'Can view session',5,'view_session'),
        (21,'Can add Token',6,'add_token'),
        (22,'Can change Token',6,'change_token'),
        (23,'Can delete Token',6,'delete_token'),
        (24,'Can view Token',6,'view_token'),
        (25,'Can add Token',7,'add_tokenproxy'),
        (26,'Can change Token',7,'change_tokenproxy'),
        (27,'Can delete Token',7,'delete_tokenproxy'),
        (28,'Can view Token',7,'view_tokenproxy'),
        (29,'Can add user',8,'add_user'),
        (30,'Can change user',8,'change_user'),
        (31,'Can delete user',8,'delete_user'),
        (32,'Can view user',8,'view_user'),
        (33,'Can add course',9,'add_course'),
        (34,'Can change course',9,'change_course'),
        (35,'Can delete course',9,'delete_course'),
        (36,'Can view course',9,'view_course'),
        (37,'Can add registration window',10,'add_registrationwindow'),
        (38,'Can change registration window',10,'change_registrationwindow'),
        (39,'Can delete registration window',10,'delete_registrationwindow'),
        (40,'Can view registration window',10,'view_registrationwindow'),
        (41,'Can add registration',11,'add_registration'),
        (42,'Can change registration',11,'change_registration'),
        (43,'Can delete registration',11,'delete_registration'),
        (44,'Can view registration',11,'view_registration'),
    ]
    with table.batch_writer() as batch:
        for pid, name, ct_id, codename in permissions:
            batch.put_item(Item={
                "id":              Decimal(pid),
                "name":            name,
                "content_type_id": Decimal(ct_id),
                "codename":        codename,
            })
    print(f"  [OK] Seed auth_permission ({len(permissions)} items)")


def seed_django_content_type(db):
    table = db.Table(tbl("django_content_type"))
    content_types = [
        (8,  'accounts',     'user'),
        (1,  'admin',        'logentry'),
        (3,  'auth',         'group'),
        (2,  'auth',         'permission'),
        (6,  'authtoken',    'token'),
        (7,  'authtoken',    'tokenproxy'),
        (4,  'contenttypes', 'contenttype'),
        (9,  'courses',      'course'),
        (11, 'courses',      'registration'),
        (10, 'courses',      'registrationwindow'),
        (5,  'sessions',     'session'),
    ]
    with table.batch_writer() as batch:
        for cid, app_label, model in content_types:
            batch.put_item(Item={
                "id":        Decimal(cid),
                "app_label": app_label,
                "model":     model,
            })
    print(f"  [OK] Seed django_content_type ({len(content_types)} items)")


def seed_django_migrations(db):
    table = db.Table(tbl("django_migrations"))
    migrations = [
        (1,  'contenttypes', '0001_initial',                        '2026-02-24T04:13:53.352782'),
        (2,  'contenttypes', '0002_remove_content_type_name',       '2026-02-24T04:13:53.417033'),
        (3,  'auth',         '0001_initial',                        '2026-02-24T04:13:53.576239'),
        (4,  'auth',         '0002_alter_permission_name_max_length','2026-02-24T04:13:53.626497'),
        (5,  'auth',         '0003_alter_user_email_max_length',    '2026-02-24T04:13:53.630082'),
        (6,  'auth',         '0004_alter_user_username_opts',       '2026-02-24T04:13:53.633156'),
        (7,  'auth',         '0005_alter_user_last_login_null',     '2026-02-24T04:13:53.636183'),
        (8,  'auth',         '0006_require_contenttypes_0002',      '2026-02-24T04:13:53.637498'),
        (9,  'auth',         '0007_alter_validators_add_error_messages','2026-02-24T04:13:53.640721'),
        (10, 'auth',         '0008_alter_user_username_max_length', '2026-02-24T04:13:53.643697'),
        (11, 'auth',         '0009_alter_user_last_name_max_length','2026-02-24T04:13:53.647812'),
        (12, 'auth',         '0010_alter_group_name_max_length',    '2026-02-24T04:13:53.655824'),
        (13, 'auth',         '0011_update_proxy_permissions',       '2026-02-24T04:13:53.660469'),
        (14, 'auth',         '0012_alter_user_first_name_max_length','2026-02-24T04:13:53.663863'),
        (15, 'accounts',     '0001_initial',                        '2026-02-24T04:13:53.859042'),
        (16, 'admin',        '0001_initial',                        '2026-02-24T04:13:53.943032'),
        (17, 'admin',        '0002_logentry_remove_auto_add',       '2026-02-24T04:13:53.950360'),
        (18, 'admin',        '0003_logentry_add_action_flag_choices','2026-02-24T04:13:53.954542'),
        (19, 'authtoken',    '0001_initial',                        '2026-02-24T04:13:54.017904'),
        (20, 'authtoken',    '0002_auto_20160226_1747',             '2026-02-24T04:13:54.032805'),
        (21, 'authtoken',    '0003_tokenproxy',                     '2026-02-24T04:13:54.036078'),
        (22, 'authtoken',    '0004_alter_tokenproxy_options',       '2026-02-24T04:13:54.039169'),
        (23, 'courses',      '0001_initial',                        '2026-02-24T04:13:54.200208'),
        (24, 'sessions',     '0001_initial',                        '2026-02-24T04:13:54.230740'),
    ]
    with table.batch_writer() as batch:
        for mid, app, name, applied in migrations:
            batch.put_item(Item={
                "id":      Decimal(mid),
                "app":     app,
                "name":    name,
                "applied": applied,
            })
    print(f"  [OK] Seed django_migrations ({len(migrations)} items)")


# ─────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────

def main():
    db = get_dynamodb_resource()

    print("\n=== Tạo bảng DynamoDB ===")
    create_tables(db)

    print("\n=== Seed dữ liệu ===")
    seed_django_content_type(db)
    seed_auth_permission(db)
    seed_django_migrations(db)
    seed_accounts_user(db)
    seed_authtoken_token(db)
    seed_courses_course(db)
    seed_courses_registration(db)
    seed_courses_registrationwindow(db)

    print("\n✓ Hoàn tất! Tất cả bảng và dữ liệu đã được khởi tạo.\n")


if __name__ == "__main__":
    main()
