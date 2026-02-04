# CI/CD Pipeline Setup với GitHub → AWS CodePipeline → ECS

## Tổng quan

Pipeline tự động:
1. **Source**: GitHub push → trigger pipeline
2. **Build**: CodeBuild build Docker image → push to ECR
3. **Deploy**: ECS deploy new image với zero-downtime

---

## Bước 1: Tạo GitHub Personal Access Token

1. Vào GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click "Generate new token (classic)"
3. Chọn scopes:
   - `repo` (Full control of private repositories)
   - `admin:repo_hook` (Full control of repository hooks)
4. Copy token (chỉ hiển thị 1 lần!)

---

## Bước 2: Store GitHub Token trong Secrets Manager

```bash
aws secretsmanager create-secret \
  --name course-registration/github-token \
  --description "GitHub personal access token for CodePipeline" \
  --secret-string '{"token":"ghp_xxxxxxxxxxxxxxxxxxxxx"}' \
  --region us-east-1
```

---

## Bước 3: Tạo CodePipeline qua Terraform

Thêm vào file `terraform/codepipeline.tf`:

```hcl
# S3 Bucket for CodePipeline Artifacts
resource "aws_s3_bucket" "codepipeline" {
  bucket = "${var.project_name}-codepipeline-artifacts-${data.aws_caller_identity.current.account_id}"

  tags = var.common_tags
}

resource "aws_s3_bucket_public_access_block" "codepipeline" {
  bucket = aws_s3_bucket.codepipeline.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# IAM Role for CodePipeline
resource "aws_iam_role" "codepipeline" {
  name = "${var.project_name}-codepipeline-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "codepipeline.amazonaws.com"
        }
      }
    ]
  })

  tags = var.common_tags
}

resource "aws_iam_role_policy" "codepipeline" {
  name = "${var.project_name}-codepipeline-policy"
  role = aws_iam_role.codepipeline.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:GetObjectVersion",
          "s3:PutObject"
        ]
        Resource = "${aws_s3_bucket.codepipeline.arn}/*"
      },
      {
        Effect = "Allow"
        Action = [
          "codebuild:BatchGetBuilds",
          "codebuild:StartBuild"
        ]
        Resource = "*"
      },
      {
        Effect = "Allow"
        Action = [
          "ecs:DescribeServices",
          "ecs:DescribeTaskDefinition",
          "ecs:DescribeTasks",
          "ecs:ListTasks",
          "ecs:RegisterTaskDefinition",
          "ecs:UpdateService"
        ]
        Resource = "*"
      },
      {
        Effect = "Allow"
        Action = [
          "iam:PassRole"
        ]
        Resource = "*"
      }
    ]
  })
}

# CodeBuild Project
resource "aws_codebuild_project" "backend" {
  name          = "${var.project_name}-backend-build"
  service_role  = aws_iam_role.codebuild.arn
  build_timeout = 20

  artifacts {
    type = "CODEPIPELINE"
  }

  environment {
    compute_type                = "BUILD_GENERAL1_SMALL"
    image                       = "aws/codebuild/standard:7.0"
    type                        = "LINUX_CONTAINER"
    privileged_mode             = true
    image_pull_credentials_type = "CODEBUILD"

    environment_variable {
      name  = "AWS_ACCOUNT_ID"
      value = data.aws_caller_identity.current.account_id
    }

    environment_variable {
      name  = "AWS_DEFAULT_REGION"
      value = var.aws_region
    }

    environment_variable {
      name  = "IMAGE_REPO_NAME"
      value = aws_ecr_repository.backend.name
    }
  }

  source {
    type      = "CODEPIPELINE"
    buildspec = "buildspec.yml"
  }

  logs_config {
    cloudwatch_logs {
      group_name = aws_cloudwatch_log_group.codebuild.name
    }
  }

  tags = var.common_tags
}

# CloudWatch Log Group for CodeBuild
resource "aws_cloudwatch_log_group" "codebuild" {
  name              = "/aws/codebuild/${var.project_name}"
  retention_in_days = 7

  tags = var.common_tags
}

# IAM Role for CodeBuild
resource "aws_iam_role" "codebuild" {
  name = "${var.project_name}-codebuild-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "codebuild.amazonaws.com"
        }
      }
    ]
  })

  tags = var.common_tags
}

resource "aws_iam_role_policy" "codebuild" {
  name = "${var.project_name}-codebuild-policy"
  role = aws_iam_role.codebuild.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = "${aws_cloudwatch_log_group.codebuild.arn}:*"
      },
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:PutObject"
        ]
        Resource = "${aws_s3_bucket.codepipeline.arn}/*"
      },
      {
        Effect = "Allow"
        Action = [
          "ecr:GetAuthorizationToken",
          "ecr:BatchCheckLayerAvailability",
          "ecr:GetDownloadUrlForLayer",
          "ecr:BatchGetImage",
          "ecr:PutImage",
          "ecr:InitiateLayerUpload",
          "ecr:UploadLayerPart",
          "ecr:CompleteLayerUpload"
        ]
        Resource = "*"
      }
    ]
  })
}

# Get GitHub token from Secrets Manager
data "aws_secretsmanager_secret_version" "github_token" {
  secret_id = "course-registration/github-token"
}

# CodePipeline
resource "aws_codepipeline" "backend" {
  name     = "${var.project_name}-backend-pipeline"
  role_arn = aws_iam_role.codepipeline.arn

  artifact_store {
    location = aws_s3_bucket.codepipeline.bucket
    type     = "S3"
  }

  stage {
    name = "Source"

    action {
      name             = "Source"
      category         = "Source"
      owner            = "ThirdParty"
      provider         = "GitHub"
      version          = "1"
      output_artifacts = ["source_output"]

      configuration = {
        Owner      = "your-github-username"  # UPDATE THIS
        Repo       = "your-repo-name"        # UPDATE THIS
        Branch     = "main"
        OAuthToken = jsondecode(data.aws_secretsmanager_secret_version.github_token.secret_string)["token"]
      }
    }
  }

  stage {
    name = "Build"

    action {
      name             = "Build"
      category         = "Build"
      owner            = "AWS"
      provider         = "CodeBuild"
      version          = "1"
      input_artifacts  = ["source_output"]
      output_artifacts = ["build_output"]

      configuration = {
        ProjectName = aws_codebuild_project.backend.name
      }
    }
  }

  stage {
    name = "Deploy"

    action {
      name            = "Deploy"
      category        = "Deploy"
      owner           = "AWS"
      provider        = "ECS"
      version         = "1"
      input_artifacts = ["build_output"]

      configuration = {
        ClusterName = aws_ecs_cluster.main.name
        ServiceName = aws_ecs_service.backend.name
        FileName    = "imagedefinitions.json"
      }
    }
  }

  tags = var.common_tags
}
```

---

## Bước 4: Deploy CI/CD Pipeline

```bash
cd terraform

# Apply CodePipeline resources
terraform apply -target=aws_codepipeline.backend

# Verify
aws codepipeline list-pipelines
aws codepipeline get-pipeline --name course-registration-backend-pipeline
```

---

## Bước 5: Test Pipeline

```bash
# Push code to GitHub
git add .
git commit -m "Test CI/CD pipeline"
git push origin main

# Check pipeline status
aws codepipeline get-pipeline-state \
  --name course-registration-backend-pipeline

# Watch CodeBuild logs
aws logs tail /aws/codebuild/course-registration --follow

# Check ECS deployment
aws ecs describe-services \
  --cluster course-registration-cluster \
  --services course-registration-backend-service
```

---

## Bước 6: Monitor Pipeline

### CloudWatch Dashboard

Add pipeline metrics to dashboard:

```hcl
# In monitoring.tf
resource "aws_cloudwatch_dashboard" "cicd" {
  dashboard_name = "${var.project_name}-cicd-dashboard"

  dashboard_body = jsonencode({
    widgets = [
      {
        type = "metric"
        properties = {
          metrics = [
            ["AWS/CodeBuild", "Builds", { stat = "Sum" }],
            [".", "FailedBuilds", { stat = "Sum" }],
            [".", "Duration", { stat = "Average" }]
          ]
          period = 300
          region = var.aws_region
          title  = "CodeBuild Metrics"
        }
      }
    ]
  })
}
```

### SNS Notifications

```hcl
# CodePipeline notifications
resource "aws_codestarnotifications_notification_rule" "pipeline" {
  name        = "${var.project_name}-pipeline-notifications"
  resource    = aws_codepipeline.backend.arn
  detail_type = "FULL"

  event_type_ids = [
    "codepipeline-pipeline-pipeline-execution-failed",
    "codepipeline-pipeline-pipeline-execution-succeeded"
  ]

  target {
    address = aws_sns_topic.alerts.arn
  }

  tags = var.common_tags
}
```

---

## Rollback Strategy

### Option 1: Manual Rollback via Console

1. Go to ECS Console → Clusters → Service
2. Update Service → Revision → Select previous task definition
3. Force new deployment

### Option 2: Rollback via CLI

```bash
# List task definitions
aws ecs list-task-definitions --family-prefix course-registration-backend

# Rollback to previous version
aws ecs update-service \
  --cluster course-registration-cluster \
  --service course-registration-backend-service \
  --task-definition course-registration-backend:10 \
  --force-new-deployment
```

### Option 3: Stop Pipeline and Redeploy

```bash
# Stop current execution
aws codepipeline stop-pipeline-execution \
  --pipeline-name course-registration-backend-pipeline \
  --pipeline-execution-id <execution-id> \
  --abandon

# Revert code and re-trigger
git revert HEAD
git push origin main
```

---

## Best Practices

1. **Use feature branches**:
   ```bash
   git checkout -b feature/new-feature
   # Make changes
   git push origin feature/new-feature
   # Create PR → Merge to main → Auto deploy
   ```

2. **Enable approval stage** (manual review before deploy):
   ```hcl
   stage {
     name = "Approve"
     
     action {
       name     = "ManualApproval"
       category = "Approval"
       owner    = "AWS"
       provider = "Manual"
       version  = "1"
       
       configuration = {
         CustomData = "Please review and approve deployment"
       }
     }
   }
   ```

3. **Use staging environment**:
   ```bash
   terraform workspace new staging
   terraform apply
   ```

4. **Implement automated testing** in CodeBuild:
   ```yaml
   # In buildspec.yml
   phases:
     pre_build:
       commands:
         - cd backend
         - pip install -r requirements.txt
         - python manage.py test
   ```

5. **Tag Docker images** with version:
   ```yaml
   - IMAGE_TAG=$CODEBUILD_BUILD_NUMBER
   - docker build -t $REPOSITORY_URI:$IMAGE_TAG .
   ```

---

## Troubleshooting

### Pipeline fails at Source stage
- Check GitHub token is valid
- Verify repository name and branch
- Check GitHub webhook is created

### Pipeline fails at Build stage
- Check CodeBuild logs
- Verify ECR permissions
- Check Dockerfile syntax
- Ensure buildspec.yml exists

### Pipeline fails at Deploy stage
- Check ECS service is running
- Verify task definition
- Check security groups
- Review ECS logs

### Slow builds
- Use Docker layer caching
- Optimize Dockerfile
- Use larger CodeBuild instance type

---

## Cost Optimization

- **CodeBuild**: ~$0.005/build minute (100 builds/month = ~$5)
- **CodePipeline**: $1/active pipeline/month
- **S3 Artifacts**: ~$0.10/month
- **Total CI/CD cost**: ~$6-10/month

Tips:
- Use BUILD_GENERAL1_SMALL for most builds
- Clean up old artifacts in S3
- Use GitHub Actions for simple builds (free for public repos)
