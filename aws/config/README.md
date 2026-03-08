# AWS Config integration (ECS + Lambda + RDS baseline)

Tài liệu này hướng dẫn bật AWS Config và triển khai bộ AWS Managed Rules baseline cho hệ thống trong repo.

## 1) Mục tiêu

- Bật AWS Config recorder + delivery channel ở từng region.
- Lưu lịch sử config vào S3 bucket tập trung.
- Tạo bộ rule baseline để kiểm soát bảo mật/compliance cho ECS, Lambda, RDS, S3, IAM, VPC.

## 2) Yêu cầu trước khi chạy

- AWS CLI đã cài và `aws configure` đúng account/profile.
- IAM identity chạy lệnh cần quyền (tối thiểu):
  - `config:*` (hoặc granular: `Put*`, `StartConfigurationRecorder`, `Describe*`)
  - `iam:CreateServiceLinkedRole`
  - `s3:CreateBucket`, `s3:PutBucketPolicy`, `s3:PutBucketVersioning`, `s3:PutEncryptionConfiguration`
  - `sts:GetCallerIdentity`

## 3) Bật AWS Config

Di chuyển vào thư mục script:

```bash
cd aws/config
chmod +x setup_config.sh deploy_baseline_rules.sh
```

Chạy bootstrap (ví dụ region `us-east-1`):

```bash
./setup_config.sh --bucket <your-config-bucket-name> --region us-east-1
```

Ví dụ có SNS topic để nhận notification:

```bash
./setup_config.sh \
  --bucket <your-config-bucket-name> \
  --region us-east-1 \
  --sns-topic-arn arn:aws:sns:us-east-1:111122223333:aws-config-alerts
```

## 4) Triển khai AWS Managed Rules baseline

```bash
./deploy_baseline_rules.sh --region us-east-1 --prefix prod
```

Rule sẽ có dạng tên: `prod-cloudtrail-enabled`, `prod-rds-storage-encrypted`, ...

### Danh sách baseline rules được tạo

1. `CLOUD_TRAIL_ENABLED`
2. `ROOT_ACCOUNT_MFA_ENABLED`
3. `IAM_USER_MFA_ENABLED`
4. `S3_BUCKET_PUBLIC_READ_PROHIBITED`
5. `S3_BUCKET_PUBLIC_WRITE_PROHIBITED`
6. `S3_BUCKET_SERVER_SIDE_ENCRYPTION_ENABLED`
7. `RDS_STORAGE_ENCRYPTED`
8. `RDS_INSTANCE_PUBLIC_ACCESS_CHECK`
9. `INCOMING_SSH_DISABLED`
10. `VPC_DEFAULT_SECURITY_GROUP_CLOSED`
11. `ECR_PRIVATE_IMAGE_SCANNING_ENABLED`
12. `ECS_CONTAINERS_NONPRIVILEGED`
13. `LAMBDA_FUNCTION_PUBLIC_ACCESS_PROHIBITED`
14. `LAMBDA_INSIDE_VPC`
15. `REQUIRED_TAGS` (`Environment`, `Owner`, `Project`)

## 5) Kiểm tra sau triển khai

```bash
aws configservice describe-configuration-recorders --region us-east-1
aws configservice describe-delivery-channels --region us-east-1
aws configservice describe-config-rules --region us-east-1 --query 'ConfigRules[].ConfigRuleName' --output table
aws configservice get-compliance-summary-by-config-rule --region us-east-1
```

Xem chi tiết các rule vi phạm:

```bash
aws configservice describe-compliance-by-config-rule \
  --region us-east-1 \
  --compliance-types NON_COMPLIANT
```

## 6) Rollout khuyến nghị

- Bật trước ở môi trường `dev/staging` để đo số lượng NON_COMPLIANT.
- Chia rule theo mức độ:
  - Critical: CloudTrail, MFA, S3 public access, RDS public access.
  - High: encryption, network hardening.
  - Medium: tagging governance.
- Sau khi ổn định mới enforce remediation tự động bằng SSM Automation.

## 7) Lỗi thường gặp

- `InsufficientPermissionsException`: thiếu IAM permissions.
- `NoAvailableConfigurationRecorderException`: chưa chạy `setup_config.sh`.
- Rule fail theo region: một số managed rule không hỗ trợ ở mọi region.
- `S3 bucket policy error`: bucket đang bị policy chặt từ trước; cần merge policy thủ công.

## 8) Mở rộng

- Dùng cùng script cho nhiều region bằng vòng lặp shell.
- Tách prefix theo môi trường (`dev`, `stg`, `prod`) để dễ quản lý.
- Tích hợp kiểm tra compliance vào CI/CD trước khi promote lên production.
