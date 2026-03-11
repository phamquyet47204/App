# Terraform Infrastructure as Code

Triển khai toàn bộ kiến trúc Course Registration Application trên AWS bằng Terraform.

## Architecture

```
Route 53 (DNS) → CloudFront + WAF
                    ↓
              ALB (HTTPS) + WAF
               ↓           ↓
        ECS/Fargate    S3 Frontend
               ↓
        DynamoDB + Redis
               ↓
           Lambda (SES)
```

## Prerequisites

1. **AWS Account** với credentials cấu hình
2. **Terraform >= 1.0**
3. **AWS CLI** để quản lý S3 state backend
4. **Domain name** đã đăng ký tại Route 53

## Quick Start

### 1. Setup Terraform Backend (S3 + DynamoDB)

```bash
cd /home/ubuntu/App/aws/terraform

# Tạo S3 bucket cho state
aws s3api create-bucket \
  --bucket course-reg-terraform-state \
  --region ap-southeast-1 \
  --create-bucket-configuration LocationConstraint=ap-southeast-1

# Enable versioning
aws s3api put-bucket-versioning \
  --bucket course-reg-terraform-state \
  --versioning-configuration Status=Enabled

# Tạo DynamoDB table cho locks
aws dynamodb create-table \
  --table-name terraform-locks \
  --attribute-definitions AttributeName=LockID,AttributeType=S \
  --key-schema AttributeName=LockID,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST \
  --region ap-southeast-1
```

### 2. Cấu hình biến

```bash
# Sửa terraform.tfvars với giá trị thực tế
domain_name = "yourdomain.com"  # Thay bằng domain của bạn
```

### 3. Khởi tạo Terraform

```bash
terraform init
```

### 4. Review Plan

```bash
terraform plan -out=tfplan
```

### 5. Triển khai

```bash
terraform apply tfplan
```

## Outputs

Sau khi apply thành công, lấy các output:

```bash
terraform output
```

**Quan trọng:**
- `ecr_repository_url` — Địa chỉ để push Docker image
- `alb_dns_name` — DNS của ALB (dùng để setup Route 53)
- `cloudfront_domain_name` — CloudFront distribution
- `frontend_bucket_name` — S3 bucket cho frontend

## Post-Deployment

### 1. Push Docker Image

```bash
# Build backend image
docker build -t <ecr_repository_url>:latest ./backend

# Login to ECR
aws ecr get-login-password --region ap-southeast-1 | \
  docker login --username AWS --password-stdin <account_id>.dkr.ecr.ap-southeast-1.amazonaws.com

# Push image
docker push <ecr_repository_url>:latest
```

### 2. Update Secrets Manager

```bash
aws secretsmanager create-secret \
  --name prod/app/backend \
  --secret-string file://secrets_backup_prod_app_backend.json \
  --region ap-southeast-1
```

### 3. Setup Route 53

Thêm records trong Route 53:
- `yourdomain.com` → CloudFront distribution
- `api.yourdomain.com` → ALB (nếu cần)

### 4. Deploy Frontend

```bash
# Build với API URL đúng
cd frontend
VITE_API_BASE_URL=https://yourdomain.com/api npm run build

# Upload lên S3
aws s3 sync dist/ s3://<frontend_bucket_name>/
```

## Module Structure

```
aws/terraform/
├── main.tf                 # Root module composition
├── variables.tf           # Input variables
├── outputs.tf             # Output values
├── versions.tf            # Provider versions
├── terraform.tfvars       # Variable values
├── modules/
│   ├── networking/        # VPC, ALB, Subnets
│   ├── security/          # Security groups, WAF, IAM
│   ├── compute/           # ECS, Fargate, ECR
│   ├── database/          # DynamoDB, Redis
│   ├── storage/           # S3, Firehose
│   └── monitoring/        # CloudWatch, CloudTrail
```

## Scaling

### Adjust ECS Auto Scaling

```bash
# Chỉnh max_capacity trong terraform.tfvars
vim terraform.tfvars
terraform plan
terraform apply
```

### Change Task Resources

```bash
# Tăng CPU/Memory
task_cpu    = "512"
task_memory = "1024"
terraform apply
```

## Monitoring

- **CloudWatch Dashboard**: `https://console.aws.amazon.com/cloudwatch/`
- **CloudTrail Logs**: S3 bucket `course-reg-cloudtrail-logs-*`
- **WAF Logs**: S3 bucket `course-reg-waf-logs-*` (via Firehose)

## Cleanup

```bash
# Xóa toàn bộ infrastructure
terraform destroy

# Xem plan trước khi xóa
terraform destroy -out=tfplan
terraform show tfplan
terraform apply tfplan
```

## Troubleshooting

### Error: ACM Certificate Validation

```bash
# Validate ACM certificate thủ công trong AWS Console
# Hoặc chỉnh domain_name trong terraform.tfvars
```

### Error: S3 Bucket Already Exists

```bash
# Bucket names phải unique globally
# Thay đổi name trong storage/main.tf
```

### Error: WAF Association Failed

```bash
# WAF phải ở cùng region
# Kiểm tra aws_region trong variables.tf
```

## Support

Xem chi tiết architecture tại `../architecture.md`
