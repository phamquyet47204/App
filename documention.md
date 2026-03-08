# Hướng dẫn triển khai AWS cho dự án (Secrets Manager → ECR → ECS + ALB)

Tài liệu này đi theo luồng triển khai thực tế: chuẩn bị secret, build và đẩy image lên ECR, sau đó triển khai ECS Fargate phía sau ALB. Nội dung được viết theo thứ tự từ dễ đến khó để có thể làm từng bước và kiểm tra ngay.

## 1) Kiến trúc mục tiêu

- **Backend**: Django (`backend/`) chạy ECS Fargate, cổng container `8000`.
- **Frontend**: Nginx + React build (`frontend/`) chạy ECS Fargate, cổng container `80`.
- **ALB**: route `/*` về frontend, route `/api/*` (và `/admin/*` nếu cần) về backend.
- **Database**: MySQL/RDS (điền thông tin DB qua secret).
- **Secrets**: AWS Secrets Manager, backend tự load vào env qua code trong `backend/config/settings.py`.

---

## 2) Chuẩn bị trước khi triển khai

Trước khi bắt đầu, bạn nên kiểm tra nhanh các điều kiện sau:

- AWS CLI đã `aws configure` đúng account/region.
- Docker đã cài.
- Quyền IAM đủ để thao tác: ECR, ECS, ELBv2, CloudWatch Logs, IAM PassRole, Secrets Manager.
- Region ví dụ: `us-east-1`.

Đặt các biến dùng chung (chạy ở local hoặc CI):

```bash
export AWS_REGION=us-east-1
export ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

export ECR_REPO_BE=app-backend
export ECR_REPO_FE=app-frontend
export IMAGE_TAG=v1

export ECS_CLUSTER=course-registration-cluster
export ECS_SERVICE_BE=course-registration-be
export ECS_SERVICE_FE=course-registration-fe
```

---

## 3) Cấu hình code để dùng AWS Secrets Manager

Backend đã hỗ trợ đọc secret từ AWS trong `backend/config/settings.py` thông qua các biến:

- `USE_AWS_SECRETS=true`
- `AWS_SECRET_NAME=<secret-name>`
- `AWS_REGION=<region>`
- `AWS_SECRETS_REQUIRED=true|false`

Khi bật `USE_AWS_SECRETS=true`, ứng dụng sẽ gọi `secretsmanager:GetSecretValue`, parse JSON và nạp từng key vào `os.environ`.

### 3.1 Tạo secret cho backend

Ví dụ tạo secret có tên `course-registration/prod/backend`:

```bash
aws secretsmanager create-secret \
  --name course-registration/prod/backend \
  --region $AWS_REGION \
  --secret-string '{
    "DJANGO_SECRET_KEY":"replace-me",
    "DJANGO_DEBUG":"False",
    "DJANGO_ALLOW_ALL_HOSTS_ON_ECS":"true",
    "DB_ENGINE":"mysql",
    "MYSQL_DB_HOST":"<rds-endpoint>",
    "MYSQL_DB_PORT":"3306",
    "MYSQL_DB_NAME":"course_registration",
    "MYSQL_DB_USER":"admin",
    "MYSQL_DB_PASSWORD":"replace-me",
    "CORS_ALLOWED_ORIGINS":"https://<your-domain>",
    "CSRF_TRUSTED_ORIGINS":"https://<your-domain>",
    "EMAIL_PROVIDER":"lambda",
    "EMAIL_LAMBDA_FUNCTION_NAME":"course-registration-ses-mail-sender",
    "EMAIL_LAMBDA_REGION":"us-east-1"
  }'
```

Nếu secret đã tồn tại thì cập nhật như sau:

```bash
aws secretsmanager put-secret-value \
  --secret-id course-registration/prod/backend \
  --region $AWS_REGION \
  --secret-string file://secret-prod.json
```

### 3.2 Quyền IAM cho ECS task role

Task role của backend cần tối thiểu các quyền sau:

- `secretsmanager:GetSecretValue` cho secret backend.
- `kms:Decrypt` nếu secret dùng KMS key custom.
- `lambda:InvokeFunction` nếu dùng `EMAIL_PROVIDER=lambda`.

Ví dụ policy tham khảo:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["secretsmanager:GetSecretValue"],
      "Resource": "arn:aws:secretsmanager:us-east-1:<account-id>:secret:course-registration/prod/backend*"
    },
    {
      "Effect": "Allow",
      "Action": ["lambda:InvokeFunction"],
      "Resource": "arn:aws:lambda:us-east-1:<account-id>:function:course-registration-ses-mail-sender"
    }
  ]
}
```

---

## 4) Build và đẩy image lên Amazon ECR

### 4.1 Login ECR

```bash
aws ecr get-login-password --region $AWS_REGION | \
  docker login --username AWS --password-stdin $ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com
```

### 4.2 Tạo repository (nếu chưa tồn tại)

```bash
aws ecr describe-repositories --repository-names $ECR_REPO_BE --region $AWS_REGION >/dev/null 2>&1 || \
aws ecr create-repository --repository-name $ECR_REPO_BE --region $AWS_REGION

aws ecr describe-repositories --repository-names $ECR_REPO_FE --region $AWS_REGION >/dev/null 2>&1 || \
aws ecr create-repository --repository-name $ECR_REPO_FE --region $AWS_REGION
```

### 4.3 Build + push backend

```bash
cd backend
docker build -t $ECR_REPO_BE:$IMAGE_TAG .
docker tag $ECR_REPO_BE:$IMAGE_TAG $ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPO_BE:$IMAGE_TAG
docker push $ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPO_BE:$IMAGE_TAG
cd ..
```

### 4.4 Build + push frontend

```bash
cd frontend
docker build -t $ECR_REPO_FE:$IMAGE_TAG .
docker tag $ECR_REPO_FE:$IMAGE_TAG $ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPO_FE:$IMAGE_TAG
docker push $ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPO_FE:$IMAGE_TAG
cd ..
```

---

## 5) Triển khai ECS Fargate + ALB

### 5.1 Tạo ECS Cluster

```bash
aws ecs create-cluster --cluster-name $ECS_CLUSTER --region $AWS_REGION
```

### 5.2 Tạo ALB + Target Groups

1. Tạo ALB internet-facing ở ít nhất 2 public subnet.
2. Tạo 2 target group kiểu **IP**:
   - `tg-frontend` port `80`
   - `tg-backend` port `8000`
3. Health check:
   - Frontend: path `/`
   - Backend: path `/api/registration-window/` (hoặc endpoint health riêng nếu có)

> Khuyến nghị Security Group:
> - ALB SG: mở `80/443` từ internet.
> - ECS Service SG: chỉ cho inbound từ ALB SG vào port `80` và `8000`.

### 5.3 Listener rules ALB

- Tạo listener `:80` hoặc `:443`.
- Rule ưu tiên cao:
  - `/api/*` → `tg-backend`
  - `/admin/*` → `tg-backend` (nếu dùng Django admin qua ALB)
- Default rule:
  - `/*` → `tg-frontend`

### 5.4 Task Definition cho backend

Container backend dùng image ECR backend với `containerPort=8000`.

Environment tối thiểu:

- `USE_AWS_SECRETS=true`
- `AWS_SECRET_NAME=course-registration/prod/backend`
- `AWS_REGION=us-east-1`
- `AWS_SECRETS_REQUIRED=true`

CloudWatch logs:

- awslogs group: `/ecs/course-registration-be`
- awslogs stream prefix: `ecs`

### 5.5 Task Definition cho frontend

Container frontend dùng image ECR frontend với `containerPort=80`.

CloudWatch logs:

- awslogs group: `/ecs/course-registration-fe`
- awslogs stream prefix: `ecs`

### 5.6 Tạo ECS Services

- Service backend gắn `tg-backend`, nên để desired count ban đầu `1` hoặc `2`.
- Service frontend gắn `tg-frontend`, nên để desired count ban đầu `1` hoặc `2`.
- Launch type: `FARGATE`.
- Network: private subnets (khuyến nghị) + NAT để pull image/call AWS APIs.

---

## 6) Cấu hình Auto Scaling cho ECS Service (khuyến nghị)

Đăng ký scalable target cho backend service:

```bash
aws application-autoscaling register-scalable-target \
  --service-namespace ecs \
  --resource-id service/$ECS_CLUSTER/$ECS_SERVICE_BE \
  --scalable-dimension ecs:service:DesiredCount \
  --min-capacity 1 \
  --max-capacity 4 \
  --region $AWS_REGION
```

Tạo policy target tracking theo CPU 60%:

```bash
aws application-autoscaling put-scaling-policy \
  --service-namespace ecs \
  --resource-id service/$ECS_CLUSTER/$ECS_SERVICE_BE \
  --scalable-dimension ecs:service:DesiredCount \
  --policy-name cpu60-backend \
  --policy-type TargetTrackingScaling \
  --target-tracking-scaling-policy-configuration '{
    "TargetValue": 60.0,
    "PredefinedMetricSpecification": {
      "PredefinedMetricType": "ECSServiceAverageCPUUtilization"
    },
    "ScaleInCooldown": 120,
    "ScaleOutCooldown": 60
  }' \
  --region $AWS_REGION
```

Kiểm tra lại cấu hình:

```bash
aws application-autoscaling describe-scalable-targets --service-namespace ecs --region $AWS_REGION
```

---

## 7) Checklist kiểm tra sau deploy

- `aws ecs describe-services` trả về service ở trạng thái `ACTIVE`, task `RUNNING`.
- Target group health đều `healthy`.
- Truy cập ALB DNS để kiểm tra:
  - `GET /` ra frontend.
  - `GET /api/registration-window/` ra API backend.
- Đăng ký/hủy môn thành công và gửi mail (nếu bật Lambda SES).
- Log backend/frontend xuất hiện ở CloudWatch Logs.

---

## 8) Lỗi thường gặp và cách nhận biết

- **502/504 từ ALB**: sai health check path/port hoặc app chưa listen đúng cổng.
- **Task crash lúc boot**: secret thiếu key bắt buộc (`MYSQL_DB_*`, `DJANGO_SECRET_KEY`, ...).
- **Không đọc được secret**: thiếu quyền `secretsmanager:GetSecretValue` ở task role.
- **Không gửi mail Lambda**: thiếu `lambda:InvokeFunction` hoặc sai `EMAIL_LAMBDA_FUNCTION_NAME`.
- **Frontend gọi API lỗi CORS/CSRF**: chưa set `CORS_ALLOWED_ORIGINS`, `CSRF_TRUSTED_ORIGINS` đúng domain ALB/custom domain.

---

## 9) Gợi ý CI/CD (tùy chọn)

Repository đã có workflow deploy ECS (`.github/workflows/cd-ecs.yml`). Có thể map theo các biến:

- `AWS_REGION`
- `ECR_REPO_BE`, `ECR_REPO_FE`
- `ECS_CLUSTER`, `ECS_SERVICE_BE`, `ECS_SERVICE_FE`
- `ECS_CONTAINER_BE`, `ECS_CONTAINER_FE`

và dùng OIDC role qua secret `AWS_ROLE_ARN`.

---

## 10) Tóm tắt nhanh luồng triển khai

1. Hoàn thiện code + bật cơ chế đọc AWS Secrets trong backend.
2. Tạo hoặc cập nhật secret JSON trên Secrets Manager.
3. Build image backend/frontend và push lên ECR.
4. Tạo ECS Task Definitions trỏ image ECR + env `USE_AWS_SECRETS`.
5. Tạo ALB, target groups, listener rules (`/api/*` về backend, còn lại frontend).
6. Tạo ECS Services và gắn target groups.
7. Bật auto scaling, kiểm tra health/logs, test chức năng end-to-end.

---

## 11) Hạng mục nên triển khai thêm cho production (WAF và các phần liên quan)

Đây là checklist hardening sau khi hệ thống đã chạy ổn định.

### 11.1 Ưu tiên cao: Bảo mật lớp biên (ALB)

1. **AWS WAF v2 gắn với ALB**
   - Bật các managed rule groups tối thiểu:
     - `AWSManagedRulesCommonRuleSet`
     - `AWSManagedRulesKnownBadInputsRuleSet`
     - `AWSManagedRulesAmazonIpReputationList`
  - Thêm rate-based rule (ví dụ giới hạn `2000 req/5 phút/IP`) để giảm brute-force và DDoS lớp ứng dụng.
   - Bật WAF logging về CloudWatch Logs hoặc S3 để điều tra sự cố.

2. **HTTPS bắt buộc**
   - Gắn ACM certificate cho ALB listener `443`.
   - Redirect toàn bộ `80 -> 443`.
   - Chỉ giữ TLS policy hiện đại (ví dụ `ELBSecurityPolicy-TLS13-1-2-2021-06`).

Ví dụ lệnh tạo Web ACL (chưa gắn rule chi tiết):

```bash
aws wafv2 create-web-acl \
  --name course-registration-web-acl \
  --scope REGIONAL \
  --default-action Allow={} \
  --visibility-config SampledRequestsEnabled=true,CloudWatchMetricsEnabled=true,MetricName=courseRegistrationWebAcl \
  --region $AWS_REGION
```

Sau đó gắn Web ACL vào ALB:

```bash
aws wafv2 associate-web-acl \
  --web-acl-arn <web-acl-arn> \
  --resource-arn <alb-arn> \
  --region $AWS_REGION
```

### 11.2 Ưu tiên cao: Bảo mật workload và dữ liệu

- Chạy ECS tasks trong **private subnets**, chỉ để ALB ở public subnets.
- Security Group theo nguyên tắc tối thiểu:
  - ALB SG nhận `80/443` từ internet.
  - ECS SG chỉ nhận từ ALB SG vào đúng port app.
  - RDS SG chỉ nhận từ ECS SG (3306), không mở public.
- Bật ECR image scanning và chặn promote image có lỗ hổng mức `Critical`.
- Dùng KMS key riêng cho secrets quan trọng; bật rotation cho DB credentials.

### 11.3 Ưu tiên trung bình: Độ ổn định và rollback

- Bật ECS deployment circuit breaker + automatic rollback.
- Đặt `healthCheckGracePeriodSeconds` phù hợp khi app khởi động chậm.
- Auto Scaling theo nhiều tín hiệu:
  - CPU
  - Memory
  - ALB RequestCountPerTarget
- Dùng RDS Multi-AZ + backup/PITR để tăng khả năng phục hồi.

### 11.4 Quan sát, tuân thủ và chi phí

- CloudWatch Alarms tối thiểu:
  - ALB `HTTPCode_Target_5XX_Count`
  - ALB latency p95
  - ECS `CPUUtilization` / `MemoryUtilization`
  - ECS task restart bất thường
- Bật và duy trì: CloudTrail, GuardDuty, Security Hub, AWS Config rules.
- Thiết lập AWS Budgets + Cost Anomaly Detection để cảnh báo chi phí bất thường.

### 11.5 Thứ tự rollout khuyến nghị

1. HTTPS + WAF managed rules + rate limit.
2. Private networking + siết Security Groups + RDS không public.
3. ECS rollback/circuit breaker + thêm alarm giám sát.
4. ECR scan gating + Security Hub/GuardDuty + cost controls.

