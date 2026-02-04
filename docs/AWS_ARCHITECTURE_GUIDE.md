# 🏗️ Hướng dẫn xây dựng kiến trúc (AWS)

> Mục tiêu: bảo mật, scale linh hoạt theo mùa ĐKMH, chi phí tối ưu cho lab.

---

## ✅ Kiến trúc tổng quan

```
User
  ↓
CloudFront (Frontend CDN)
  ↓
S3 (Static SPA)

User
  ↓
ALB (HTTPS)
  ↓
ECS Fargate (Django API)
  ↓
Aurora MySQL Serverless v2
  ↓
ElastiCache Redis (Session/Cache)
  ↓
SES (Email)
```

---

## 📌 1. Networking (Terraform)

**Tạo bằng Terraform**:
- VPC (10.0.0.0/16)
- Public subnets (ALB)
- Private subnets (ECS, RDS, Redis)
- Internet Gateway
- NAT Gateway
- Security Groups (ALB, ECS, Aurora, Redis)

📄 Xem: [terraform/TERRAFORM_VPC_ONLY.md](../terraform/TERRAFORM_VPC_ONLY.md)

---

## 🧭 Hướng dẫn thao tác Console chi tiết

> Dùng các ID từ Terraform outputs: VPC, subnets, security groups.

### A. RDS Aurora MySQL Serverless v2
1. AWS Console → RDS → Databases → Create database
2. Engine: Aurora MySQL 8.0
3. Template: Dev/Test
4. DB cluster identifier: `course-registration-db`
5. Credentials: admin / mật khẩu mạnh
6. Connectivity:
  - VPC: chọn VPC đã tạo
  - Subnet group: chọn private subnets
  - Public access: No
  - SG: chọn Aurora SG
7. Capacity: Serverless v2 (Min 0.5, Max 2.0 ACU)
8. Backup: 7 days, bật encryption
9. Create database → lưu Endpoint

### B. ElastiCache Redis
1. Console → ElastiCache → Redis → Create
2. Deployment: Cluster mode disabled
3. Name: `course-registration-redis`
4. Node type: `cache.t3.micro`
5. Replicas: 0 (lab) hoặc 1 (HA)
6. VPC/Subnet: private subnets
7. SG: Redis SG
8. Create → lưu Primary Endpoint

### C. ECR Repositories
1. Console → ECR → Repositories → Create
2. Backend repo: `course-registration/backend`
3. Frontend repo: `course-registration/frontend`
4. Bật scan on push

### D. IAM Roles (ECS)
1. Console → IAM → Roles → Create role
2. Trusted entity: ECS Task
3. Role 1: `ecsTaskExecutionRole` with `AmazonECSTaskExecutionRolePolicy`
4. Role 2: `ecsTaskRole` with SES + Logs permissions

### E. Secrets Manager
1. Console → Secrets Manager → Store a new secret
2. Create secrets:
  - `course-registration/db-password`
  - `course-registration/django-secret`
3. Lưu ARN để gắn vào Task Definition

### F. ECS Cluster + Task Definition
1. Console → ECS → Clusters → Create cluster (Fargate)
2. Task Definitions → Create:
  - Family: `course-registration-backend`
  - CPU: 256, Memory: 512
  - Container: backend, port 8000
  - Image: ECR backend image
  - Env: DB host/user/name + DEBUG=False
  - Secrets: DB password + SECRET_KEY
  - Log group: `/ecs/course-registration`

### G. ALB + Target Group
1. EC2 → Load Balancers → Create ALB
2. Scheme: internet-facing, VPC: chọn VPC
3. Subnets: public subnets
4. SG: ALB SG
5. Target Group: HTTP, port 8000, health path `/api/`
6. Listener: HTTP:80 → forward to target group

### H. ECS Service
1. ECS → Clusters → Services → Create
2. Service name: `backend`
3. Task definition: `course-registration-backend`
4. Desired tasks: 1
5. Network: private subnets, SG = ECS SG
6. Load balancer: chọn ALB + target group
7. Create service

### I. S3 + CloudFront (Frontend)
1. S3 → Create bucket (private)
2. Upload frontend build (`dist/`)
3. CloudFront → Create distribution
4. Origin: S3 bucket, Viewer HTTPS only
5. Cache: default settings, enable compression

### J. WAF
1. WAF & Shield → Web ACLs → Create
2. Add AWS Managed Rules + rate limit
3. Associate with ALB

### K. CloudWatch
1. Logs: tạo log group `/ecs/course-registration`
2. Alarms: CPU/Memory/5xx errors

---

## 📌 2. Load Balancer (Console)

- ALB (internet-facing)
- Listener HTTP/HTTPS
- Target Group: `/api/` health check
- SG: ALB SG

---

## 📌 3. Compute (ECS Fargate)

- Cluster: `course-registration`
- Task: 0.25 vCPU, 512MB
- Desired tasks: 1
- Auto Scaling: 1–5 tasks
- SG: ECS SG

---

## 📌 4. Database (Aurora Serverless v2)

- Engine: Aurora MySQL 8.0
- Scaling: 0.5 → 2 ACU
- Multi-AZ
- SG: Aurora SG
- Backup: 7 ngày

---

## 📌 5. Cache (ElastiCache Redis)

- Node: `cache.t3.micro`
- 1 node (lab) hoặc 2 nodes (HA)
- SG: Redis SG

---

## 📌 6. Storage + CDN

- S3: chứa frontend build
- CloudFront: CDN, HTTPS
- Cache-Control cho static assets

---

## 📌 7. Email (SES)

- Verify domain
- Move to production access
- SMTP hoặc API

---

## 📌 8. Observability

- CloudWatch Logs + Alarms
- VPC Flow Logs
- CloudTrail

---

## 📌 9. Security

- WAF (rate limit, SQLi/XSS)
- TLS/HTTPS everywhere
- Secrets Manager
- Least privilege IAM

---

## 📌 10. CI/CD (optional)

- GitHub Actions hoặc CodePipeline
- Build Docker → ECR → ECS update

---

## ✅ Lab Scaling Reference

| Layer | Min | Max |
|------|-----|-----|
| ECS Tasks | 1 | 5 |
| Aurora ACU | 0.5 | 2.0 |
| Redis Nodes | 1 | 2 |

---

## 🚀 Next Steps

1. Deploy VPC + SGs bằng Terraform
2. Tạo Aurora + Redis + ECS bằng Console
3. Deploy frontend lên S3 + CloudFront
4. (Optional) Setup CI/CD

