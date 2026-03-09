# Tài liệu triển khai chi tiết từng click chuột (AWS Console-first)

Thứ tự cố định: coding -> database -> Secrets Manager -> push ECR -> ECS -> Target Group -> ALB -> Auto Scaling -> CloudFront + WAF -> Route 53 -> CloudWatch metric + log WAF vào S3.

## 1) Coding

1. Mở code local, hoàn tất backend trong `backend/`.
2. Hoàn tất frontend trong `frontend/`.
3. Đảm bảo app chạy local trước khi deploy.

## 2) Thiết lập Database (RDS MySQL - click-by-click)

1. Vào AWS Console, chọn region (góc phải trên): `us-east-1`.
2. Gõ tìm kiếm `RDS`, click `RDS`.
3. Ở menu trái, click `Databases`.
4. Click nút `Create database`.
5. Mục `Choose a database creation method`, chọn `Standard create`.
6. Mục `Engine options`, chọn `MySQL`.
7. Mục `Templates`, chọn `Production` (hoặc `Dev/Test` nếu môi trường test).
8. Mục `Settings`:
   - DB instance identifier: nhập `course-registration-db`.
   - Master username: nhập user DB.
   - Master password: nhập password DB.
9. Mục `Connectivity`:
   - VPC: chọn VPC dùng cho ECS.
   - Public access: chọn `No`.
   - VPC security group: chọn `Choose existing`.
   - Existing security groups: chọn SG DB (SG này chỉ cho phép inbound `3306` từ SG ECS).
10. Cuộn xuống cuối, click `Create database`.
11. Sau khi tạo xong, click vào DB vừa tạo.
12. Tab `Connectivity & security`, copy `Endpoint` (sẽ dùng ở bước Secrets Manager).

## 3) Secrets Manager (click-by-click)

1. Gõ tìm kiếm `Secrets Manager`, click `Secrets Manager`.
2. Click `Store a new secret`.
3. Mục `Secret type`, chọn `Other type of secret`.
4. Mục key/value, thêm từng dòng:
   - `DJANGO_SECRET_KEY` = giá trị secret key.
   - `DJANGO_DEBUG` = `False`.
   - `DJANGO_ALLOW_ALL_HOSTS_ON_ECS` = `true`.
   - `MYSQL_DB_HOST` = endpoint RDS ở bước 2.
   - `MYSQL_DB_PORT` = `3306`.
   - `MYSQL_DB_NAME` = `course_registration`.
   - `MYSQL_DB_USER` = user DB.
   - `MYSQL_DB_PASSWORD` = password DB.
5. Click `Next`.
6. Mục `Secret name`, nhập `course-registration/prod/backend`.
7. Click `Next`.
8. Mục rotation, để mặc định (không bật nếu chưa dùng).
9. Click `Next`.
10. Màn review, click `Store`.

## 4) Push image lên ECR

### 4.1 Tạo repository trên Console

1. Gõ tìm kiếm `ECR`, click `Elastic Container Registry`.
2. Menu trái, click `Repositories`.
3. Click `Create repository`.
4. Repository name: nhập `app-backend`.
5. Bật `Scan on push` (nếu có).
6. Click `Create repository`.
7. Lặp lại tương tự để tạo `app-frontend`.

### 4.2 Push image bằng CLI (bất khả kháng)

```bash
export AWS_REGION=us-east-1
export ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
export IMAGE_TAG=v1

aws ecr get-login-password --region "$AWS_REGION" | \
docker login --username AWS --password-stdin "$ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com"

cd backend
docker build -t app-backend:$IMAGE_TAG .
docker tag app-backend:$IMAGE_TAG $ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/app-backend:$IMAGE_TAG
docker push $ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/app-backend:$IMAGE_TAG
cd ..

cd frontend
docker build -t app-frontend:$IMAGE_TAG .
docker tag app-frontend:$IMAGE_TAG $ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/app-frontend:$IMAGE_TAG
docker push $ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/app-frontend:$IMAGE_TAG
cd ..
```

## 5) Triển khai ECS (click-by-click)

### 5.1 Tạo ECS Cluster

1. Gõ `ECS`, click `Elastic Container Service`.
2. Menu trái, click `Clusters`.
3. Click `Create cluster`.
4. Cluster name: `course-registration-cluster`.
5. Click `Create`.

### 5.2 Tạo Task Definition backend

1. Menu trái, click `Task definitions`.
2. Click `Create new task definition`.
3. Chọn launch type `Fargate`, click `Next`.
4. Family: `course-registration-be`.
5. Task role: chọn role có quyền đọc secret.
6. Task execution role: chọn `ecsTaskExecutionRole`.
7. CPU/Memory: chọn `0.5 vCPU` và `1 GB`.
8. Mục `Container - 1`, click `Add container` (hoặc chỉnh container mặc định):
   - Name: `backend`
   - Image URI: `<account>.dkr.ecr.<region>.amazonaws.com/app-backend:v1`
   - Container port: `8000`
9. Mục Environment variables, thêm:
   - `USE_AWS_SECRETS` = `true`
   - `AWS_SECRET_NAME` = `course-registration/prod/backend`
   - `AWS_REGION` = `us-east-1`
   - `AWS_SECRETS_REQUIRED` = `true`
10. Mục Logging:
   - Log driver: `awslogs`
   - Log group: `/ecs/course-registration-be`
   - Stream prefix: `ecs`
11. Click `Add`/`Create` container.
12. Click `Create` task definition.

### 5.3 Tạo Task Definition frontend

1. Vẫn trong `Task definitions`, click `Create new task definition`.
2. Launch type: `Fargate`.
3. Family: `course-registration-fe`.
4. Task execution role: `ecsTaskExecutionRole`.
5. CPU/Memory: `0.25 vCPU` và `0.5 GB`.
6. Container:
   - Name: `frontend`
   - Image URI: `<account>.dkr.ecr.<region>.amazonaws.com/app-frontend:v1`
   - Container port: `80`
7. Logging:
   - Log group: `/ecs/course-registration-fe`
   - Stream prefix: `ecs`
8. Click `Create` task definition.

### 5.4 Tạo ECS Service backend

1. Menu trái `Clusters`, click `course-registration-cluster`.
2. Tab `Services`, click `Create`.
3. Launch type: `Fargate`.
4. Task definition family: chọn `course-registration-be`.
5. Service name: `course-registration-be`.
6. Desired tasks: `1`.
7. Networking:
   - Chọn VPC đúng.
   - Chọn 2 private subnets.
   - Security groups: SG cho ECS service.
   - Auto-assign public IP: `Disabled`.
8. Load balancing:
   - Chọn `Application Load Balancer`.
   - Chọn target group backend (tạo ở bước 6).
   - Container name/port: `backend:8000`.
9. Click `Create`.

### 5.5 Tạo ECS Service frontend

1. Trong cluster, tab `Services`, click `Create`.
2. Launch type: `Fargate`.
3. Task definition family: `course-registration-fe`.
4. Service name: `course-registration-fe`.
5. Desired tasks: `1`.
6. Networking giống backend (private subnet + SG ECS).
7. Load balancing chọn target group frontend, container `frontend:80`.
8. Click `Create`.

## 6) Cấu hình Target Group (click-by-click)

1. Gõ `EC2`, click `EC2`.
2. Menu trái, phần `Load Balancing`, click `Target Groups`.
3. Click `Create target group`.
4. Target type: chọn `IP addresses`.
5. Name: `course-registration-tg-be`.
6. Protocol/Port: `HTTP` và `8000`.
7. VPC: chọn VPC của ECS.
8. Health checks -> path: nhập `/api/registration-window/`.
9. Click `Next`, không cần register thủ công target (ECS tự gắn).
10. Click `Create target group`.
11. Lặp lại để tạo `course-registration-tg-fe` với:
    - Port `80`
    - Health check path `/`

## 7) Cấu hình ALB (click-by-click)

1. Trong `EC2`, menu trái `Load Balancers`.
2. Click `Create Load Balancer`.
3. Chọn `Application Load Balancer`, click `Create`.
4. Name: `course-registration-alb`.
5. Scheme: `Internet-facing`.
6. IP address type: `IPv4`.
7. Network mapping:
   - Chọn VPC.
   - Tick ít nhất 2 AZ public subnet.
8. Security groups: chọn SG ALB (mở 80/443).
9. Listener and routing:
   - Listener 80 default forward tới `course-registration-tg-fe`.
10. Click `Create load balancer`.
11. Sau khi tạo ALB xong, vào tab `Listeners and rules`, chọn listener `:80`, click `View/edit rules`.
12. Click `+` -> `Insert rule`:
   - If path is `/api/*` -> Forward to `course-registration-tg-be`.
   - Save.
13. Tạo thêm 1 rule:
   - If path is `/admin/*` -> Forward to `course-registration-tg-be`.
   - Save.
14. Đảm bảo default rule vẫn forward `course-registration-tg-fe`.

## 8) Cấu hình Auto Scaling ECS (click-by-click)

1. Vào `ECS -> Clusters -> course-registration-cluster`.
2. Tab `Services`, click service `course-registration-be`.
3. Click `Update service`.
4. Tìm phần `Auto Scaling`.
5. Tick `Configure Service Auto Scaling`.
6. Minimum number of tasks: `1`.
7. Maximum number of tasks: `4`.
8. Policy type: `Target tracking`.
9. Metric type: `ECS service average CPU utilization`.
10. Target value: `60`.
11. Click `Update`.

## 9) CloudFront + WAF (click-by-click)

### 9.1 Tạo CloudFront distribution

1. Gõ `CloudFront`, click `CloudFront`.
2. Click `Create distribution`.
3. Mục `Origin domain`, chọn ALB DNS name.
4. Mục `Viewer protocol policy`, chọn `Redirect HTTP to HTTPS`.
5. Mục `Alternate domain name (CNAME)`:
   - Add item, nhập domain app (ví dụ `app.yourdomain.com`).
6. Mục `Custom SSL certificate`, chọn certificate từ ACM.
7. Click `Create distribution`.
8. Chờ status `Deployed`.

### 9.2 Tạo và gắn WAF Web ACL

1. Gõ `WAF`, click `WAF & Shield`.
2. Menu trái `Web ACLs`, click `Create web ACL`.
3. Name: `course-registration-web-acl`.
4. Region/Scope: chọn `CloudFront (Global)`.
5. Resource to protect: chọn CloudFront distribution vừa tạo.
6. Click `Next`.
7. Add rules -> `Add managed rule groups` -> `AWS managed rule groups`.
8. Chọn tối thiểu:
   - `AWSManagedRulesCommonRuleSet`
   - `AWSManagedRulesKnownBadInputsRuleSet`
   - `AWSManagedRulesAmazonIpReputationList`
9. Click `Add rules` -> `Next` -> `Next`.
10. Click `Create web ACL`.

## 10) Route 53 (click-by-click)

1. Gõ `Route 53`, click `Route 53`.
2. Menu trái `Hosted zones`, click domain zone của bạn.
3. Click `Create record`.
4. Record name: nhập `app` (hoặc để trống nếu dùng root domain).
5. Record type: chọn `A`.
6. Bật `Alias` = `On`.
7. Route traffic to: chọn `Alias to CloudFront distribution`.
8. Chọn distribution đã tạo ở bước 9.
9. Click `Create records`.

## 11) CloudWatch metric + log WAF vào S3 (click-by-click)

### 11.1 Tạo CloudWatch Alarm cho ECS, ALB, WAF

1. Gõ `CloudWatch`, click `CloudWatch`.
2. Menu trái `Metrics`.
3. ECS metrics:
   - Click namespace `ECS` -> `ClusterName,ServiceName`.
   - Tick `CPUUtilization` và `MemoryUtilization`.
4. Với từng metric cần alarm:
   - Click `Create alarm`.
   - Chọn threshold theo ngưỡng vận hành.
   - Click `Next` -> chọn SNS topic (nếu có) -> `Next`.
   - Alarm name -> `Create alarm`.
5. ALB metrics:
   - Namespace `ApplicationELB`.
   - Chọn `HTTPCode_Target_5XX_Count`, `TargetResponseTime`.
   - Tạo alarm tương tự.
6. WAF metrics:
   - Namespace `WAFV2`.
   - Chọn `AllowedRequests`, `BlockedRequests`.
   - Tạo alarm tương tự.

### 11.2 Ghi log WAF vào S3 (qua Firehose)

1. Gõ `S3`, click `S3`.
2. Click `Create bucket`.
3. Bucket name: ví dụ `waf-logs-<account>-<region>`.
4. Click `Create bucket`.
5. Gõ `Firehose`, click `Amazon Data Firehose`.
6. Click `Create Firehose stream`.
7. Source: chọn `Direct PUT`.
8. Destination: chọn `Amazon S3`.
9. S3 destination: chọn bucket log WAF ở trên.
10. Các mục khác giữ mặc định phù hợp.
11. Click `Create Firehose stream`.
12. Quay lại `WAF & Shield` -> `Web ACLs` -> chọn `course-registration-web-acl`.
13. Tab `Logging and metrics`.
14. Click `Enable logging`.
15. Chọn Firehose stream vừa tạo.
16. Click `Save`.
17. Quay lại S3 bucket, mở tab `Objects`, xác nhận có file log mới.

## 12) Cách chứng tỏ hệ thống hoạt động (click-by-click)

1. Mở domain app trên trình duyệt.
2. Xác nhận frontend tải thành công.
3. Kiểm tra API chính trả dữ liệu (qua UI hoặc endpoint `/api/registration-window/`).
4. Vào `ECS -> Clusters -> course-registration-cluster -> Services`:
   - Backend `Running = Desired`.
   - Frontend `Running = Desired`.
5. Vào `EC2 -> Target Groups`:
   - `course-registration-tg-be` -> tab `Targets` -> trạng thái `healthy`.
   - `course-registration-tg-fe` -> tab `Targets` -> trạng thái `healthy`.
6. Vào `CloudFront -> Distribution -> Monitoring`:
   - Có request count > 0.
7. Vào `CloudWatch -> Metrics`:
   - ECS/ALB/WAF có dữ liệu metric.
8. Vào `WAF -> Web ACL -> Overview`:
   - Có `AllowedRequests`/`BlockedRequests`.
9. Vào `S3 -> bucket log WAF -> Objects`:
   - Có file log mới phát sinh.

