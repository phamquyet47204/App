# 🔁 Hướng dẫn CI/CD (GitHub Actions → ECR → ECS → S3/CloudFront)

> Mục tiêu: push code lên GitHub → tự động build & deploy backend + frontend.

---

## ✅ Tổng quan luồng CI/CD

```
Push to GitHub (main)
  ↓
GitHub Actions
  ├─ Build Docker backend → Push ECR
  ├─ Build frontend → Upload S3
  └─ Update ECS Service + Invalidate CloudFront
```

---

## 1) Chuẩn bị AWS

### 1.1 Tạo IAM User cho CI/CD
Console → IAM → Users → Create user

**Attach policies**:
- AmazonEC2ContainerRegistryFullAccess
- AmazonECS_FullAccess
- AmazonS3FullAccess
- CloudFrontFullAccess
- CloudWatchLogsFullAccess

### 1.2 Tạo Access Keys
IAM → Users → Security credentials → Create access key

Lưu:
```
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
```

---

## 2) Chuẩn bị GitHub Secrets

Repo → Settings → Secrets and variables → Actions

Add:
```
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
AWS_REGION=us-east-1
ECR_REGISTRY=xxxxxx.dkr.ecr.us-east-1.amazonaws.com
S3_BUCKET=course-registration-frontend-lab-xxxxx
CLOUDFRONT_ID=E1234ABCD
```

---

## 3) Tạo workflow file

**Path**: `.github/workflows/deploy.yml`

```yaml
name: Build & Deploy

on:
  push:
    branches: [main]
  workflow_dispatch:

env:
  AWS_REGION: us-east-1
  ECR_REGISTRY: ${{ secrets.ECR_REGISTRY }}
  BACKEND_ECR_REPO: course-registration/backend
  ECS_CLUSTER: course-registration
  ECS_SERVICE: backend

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - uses: aws-actions/configure-aws-credentials@v2
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: ${{ env.AWS_REGION }}

      - name: Login to ECR
        run: |
          aws ecr get-login-password --region ${{ env.AWS_REGION }} | \
          docker login --username AWS --password-stdin ${{ env.ECR_REGISTRY }}

      - name: Build & Push Backend
        run: |
          docker build -t backend:latest ./backend
          docker tag backend:latest ${{ env.ECR_REGISTRY }}/${{ env.BACKEND_ECR_REPO }}:latest
          docker push ${{ env.ECR_REGISTRY }}/${{ env.BACKEND_ECR_REPO }}:latest

      - name: Deploy Backend to ECS
        run: |
          aws ecs update-service \
            --cluster ${{ env.ECS_CLUSTER }} \
            --service ${{ env.ECS_SERVICE }} \
            --force-new-deployment

      - name: Build Frontend
        run: |
          cd frontend
          npm ci
          npm run build

      - name: Upload Frontend to S3
        run: |
          aws s3 sync frontend/dist/ s3://${{ secrets.S3_BUCKET }}/ --delete \
            --cache-control "public, max-age=31536000" --exclude "index.html"
          aws s3 cp frontend/dist/index.html s3://${{ secrets.S3_BUCKET }}/index.html \
            --cache-control "public, max-age=3600" --content-type "text/html"

      - name: Invalidate CloudFront
        run: |
          aws cloudfront create-invalidation \
            --distribution-id ${{ secrets.CLOUDFRONT_ID }} \
            --paths "/*"
```

---

## 4) Verify

- GitHub → Actions tab → check workflow
- ECS → Services → Deployments
- S3 → Files updated
- CloudFront → Status: Deployed

---

## ✅ Lưu ý

- Nếu dùng tag version: thêm tag trong docker build/push
- Nếu cần rollback: ECS → Deployments → chọn revision cũ
- Muốn staging/prod: tách branch + workflow

