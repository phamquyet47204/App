# Terraform - Cost Optimization

Module này triển khai đúng 3 hạng mục tối ưu chi phí đã chốt trong tài liệu:

1. VPC Endpoints:
   - S3 Gateway Endpoint
   - ECR API Interface Endpoint
   - ECR DKR Interface Endpoint
   - CloudWatch Logs Interface Endpoint
2. CloudWatch Logs retention policy
3. ECR lifecycle policy

## 1) Chuẩn bị

```bash
cd aws/terraform/cost_optimization
cp terraform.tfvars.example terraform.tfvars
```

Sửa `terraform.tfvars` theo hạ tầng thực tế.

## 2) Init / Plan / Apply

```bash
terraform init
terraform plan
terraform apply
```

## 3) Lưu ý quan trọng với CloudWatch Log Group đã tồn tại

Nếu log group đã được tạo trước đó (ví dụ ECS đã chạy), cần import trước khi apply để tránh lỗi `ResourceAlreadyExistsException`.

Ví dụ:

```bash
terraform import 'aws_cloudwatch_log_group.retention["/ecs/course-registration-be"]' '/ecs/course-registration-be'
terraform import 'aws_cloudwatch_log_group.retention["/ecs/course-registration-fe"]' '/ecs/course-registration-fe'
```

Sau đó chạy lại:

```bash
terraform plan
terraform apply
```

## 4) Security Group cho Interface Endpoints

`endpoint_security_group_id` phải cho phép inbound `443` từ security group ECS service.

## 5) Kết quả mong đợi

- ECS pull image và ghi logs qua endpoint nội bộ (giảm data qua NAT)
- Log groups có retention theo cấu hình
- ECR tự động xóa image cũ, giữ số lượng bản gần nhất
