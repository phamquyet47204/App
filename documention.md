# Hướng dẫn triển khai ưu tiên AWS Console (giảm tối đa CLI)

Mục tiêu tài liệu này: thao tác chính trên **AWS Management Console**. Chỉ dùng CLI ở các bước bắt buộc như build/push Docker image và kiểm tra nhanh.

## 1) Bạn chỉ cần dùng CLI ở 3 chỗ

1. Build + push Docker image lên ECR.
2. Test nhanh endpoint bằng `curl` (không bắt buộc).
3. (Tùy chọn) chạy script AWS Config có sẵn trong repo.

Các bước còn lại làm trên giao diện AWS Console.

---

## 2) Chuẩn bị trên AWS Console

### 2.1 Chọn region

- Vào AWS Console, góc phải trên chọn region (khuyên dùng `us-east-1` để đồng bộ toàn hệ thống).

### 2.2 Tạo/kiểm tra IAM role

Vào `IAM -> Roles`:

- Role 1: `ecsTaskExecutionRole` (nếu chưa có thì tạo theo wizard ECS Task Execution).
- Role 2: role cho app backend (ví dụ `course-registration-task-role`) và gắn policy:
  - `secretsmanager:GetSecretValue` cho secret backend.
  - `lambda:InvokeFunction` nếu gửi mail qua Lambda.

### 2.3 Tạo Secret trên Console

Vào `Secrets Manager -> Store a new secret`:

- Secret type: `Other type of secret`.
- Nhập key/value:
  - `DJANGO_SECRET_KEY`
  - `MYSQL_DB_HOST`, `MYSQL_DB_PORT`, `MYSQL_DB_NAME`, `MYSQL_DB_USER`, `MYSQL_DB_PASSWORD`
  - `DJANGO_DEBUG=False`
  - `DJANGO_ALLOW_ALL_HOSTS_ON_ECS=true`
  - `EMAIL_PROVIDER=lambda`
  - `EMAIL_LAMBDA_FUNCTION_NAME=course-registration-ses-mail-sender`
  - `EMAIL_LAMBDA_REGION=us-east-1`
- Secret name: `course-registration/prod/backend`.
- Bấm `Store`.

---

## 3) Tạo ECR repository trên Console

Vào `ECR -> Repositories -> Create repository`:

- Tạo `app-backend`.
- Tạo `app-frontend`.
- Bật `Scan on push` nếu có.

---

## 4) Build + Push image (CLI bắt buộc)

Chạy ở máy local trong thư mục `App/`.

```bash
export AWS_REGION=us-east-1
export ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
export IMAGE_TAG=v1
```

### 4.1 Login ECR

```bash
aws ecr get-login-password --region "$AWS_REGION" | \
docker login --username AWS --password-stdin "$ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com"
```

### 4.2 Push backend

```bash
cd backend
docker build -t app-backend:$IMAGE_TAG .
docker tag app-backend:$IMAGE_TAG $ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/app-backend:$IMAGE_TAG
docker push $ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/app-backend:$IMAGE_TAG
cd ..
```

### 4.3 Push frontend

```bash
cd frontend
docker build -t app-frontend:$IMAGE_TAG .
docker tag app-frontend:$IMAGE_TAG $ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/app-frontend:$IMAGE_TAG
docker push $ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/app-frontend:$IMAGE_TAG
cd ..
```

---

## 5) Tạo hạ tầng mạng trên AWS Console

## 5.1 Security Groups

Vào `EC2 -> Security Groups`:

- `alb-sg`
  - Inbound: `80` (và `443` nếu HTTPS) từ `0.0.0.0/0`.
- `ecs-service-sg`
  - Inbound `80` từ `alb-sg`.
  - Inbound `8000` từ `alb-sg`.

## 5.2 Application Load Balancer

Vào `EC2 -> Load Balancers -> Create`:

- Type: `Application Load Balancer`.
- Scheme: `Internet-facing`.
- Chọn ít nhất 2 public subnets.
- Gắn `alb-sg`.

## 5.3 Target Groups

Vào `EC2 -> Target Groups -> Create target group`:

- `course-registration-tg-fe`
  - Target type: `IP`
  - Protocol/Port: `HTTP:80`
  - Health check path: `/`

- `course-registration-tg-be`
  - Target type: `IP`
  - Protocol/Port: `HTTP:8000`
  - Health check path: `/api/registration-window/`

## 5.4 Listener Rule

Trong ALB Listener `:80`:

- Default action -> forward `course-registration-tg-fe`.
- Add rule:
  - Nếu path `/api/*` -> forward `course-registration-tg-be`.
  - Nếu path `/admin/*` -> forward `course-registration-tg-be`.

---

## 6) Tạo ECS Cluster, Task Definition, Service trên Console

## 6.1 Tạo ECS Cluster

Vào `ECS -> Clusters -> Create cluster`:

- Cluster name: `course-registration-cluster`.

## 6.2 Tạo Task Definition backend

Vào `ECS -> Task definitions -> Create`:

- Launch type: `FARGATE`.
- Family: `course-registration-be`.
- CPU/Memory: `0.5 vCPU / 1GB`.
- Task execution role: `ecsTaskExecutionRole`.
- Task role: `course-registration-task-role`.
- Container:
  - Name: `backend`
  - Image URI: `<account>.dkr.ecr.<region>.amazonaws.com/app-backend:v1`
  - Port mapping: `8000`
  - Environment variables:
    - `USE_AWS_SECRETS=true`
    - `AWS_SECRET_NAME=course-registration/prod/backend`
    - `AWS_REGION=us-east-1`
    - `AWS_SECRETS_REQUIRED=true`
  - Logging: `awslogs`, group `/ecs/course-registration-be`, stream prefix `ecs`.

## 6.3 Tạo Task Definition frontend

- Family: `course-registration-fe`.
- CPU/Memory: `0.25 vCPU / 0.5GB`.
- Container:
  - Name: `frontend`
  - Image URI: `<account>.dkr.ecr.<region>.amazonaws.com/app-frontend:v1`
  - Port mapping: `80`
  - Logging: `/ecs/course-registration-fe`.

## 6.4 Tạo ECS Service backend

Trong cluster `course-registration-cluster -> Create service`:

- Launch type: `Fargate`.
- Task definition: `course-registration-be`.
- Service name: `course-registration-be`.
- Desired tasks: `1`.
- Networking:
  - Chọn private subnets.
  - Security group: `ecs-service-sg`.
  - Auto-assign public IP: `DISABLED`.
- Load balancing:
  - Attach to existing ALB.
  - Target group: `course-registration-tg-be`.
  - Container name/port: `backend:8000`.

## 6.5 Tạo ECS Service frontend

- Task definition: `course-registration-fe`.
- Service name: `course-registration-fe`.
- Desired tasks: `1`.
- Networking tương tự backend.
- Load balancing -> target group `course-registration-tg-fe`, container `frontend:80`.

---

## 7) Bật Auto Scaling (Console)

Trong ECS service backend:

- Tab `Auto Scaling` -> `Use service auto scaling`.
- Min tasks: `1`, Max tasks: `4`.
- Policy: target tracking theo `ECS service average CPU utilization`.
- Target value: `60%`.

---

## 8) Kiểm tra sau deploy (ưu tiên Console)

1. ECS service trạng thái `Active`, task `Running`.
2. Target group health = `healthy`.
3. Mở ALB DNS:
   - `/` trả frontend.
   - `/api/registration-window/` trả JSON backend.
4. CloudWatch Logs có log từ 2 service.

CLI kiểm tra nhanh (không bắt buộc):

```bash
curl -i http://<alb-dns>/
curl -i http://<alb-dns>/api/registration-window/
```

---

## 9) Deploy bản mới bằng Console (ít CLI nhất)

1. Build/push image mới bằng CLI (bước 4) với tag mới, ví dụ `v2`.
2. Vào `ECS -> Task Definitions` tạo revision mới, đổi image tag sang `v2`.
3. Vào từng service -> `Update service` -> chọn revision mới -> Deploy.

---

## 10) Rollback bằng Console

1. Vào `ECS -> Services -> Update`.
2. Chọn lại task definition revision cũ ổn định.
3. Deploy lại và theo dõi tab `Deployments`.

---

## 11) Phần nào bắt buộc CLI?

- Build/push Docker image: hiện là bắt buộc nếu chưa có pipeline CI/CD tự đẩy image.
- Nếu bạn dùng GitHub Actions `cd-ecs.yml` sẵn có trong repo, có thể bỏ cả bước này trên local.

---

## 12) Lỗi thường gặp

- `Task stop ngay`: thiếu biến trong secret hoặc role không đọc được secret.
- `Unhealthy target`: sai port mapping (`8000` backend, `80` frontend) hoặc sai health check path.
- `502/504`: SG chưa mở luồng `ALB SG -> ECS SG` đúng port.
- `AccessDenied`: thiếu quyền IAM với ECS/ECR/ELB/Secrets Manager/IAM PassRole.

