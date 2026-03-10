variable "aws_region" {
  description = "AWS region to deploy resources"
  type        = string
  default     = "us-east-1"
}

variable "vpc_id" {
  description = "VPC ID where ECS private subnets are located"
  type        = string
}

variable "private_subnet_ids" {
  description = "Private subnet IDs used by ECS services"
  type        = list(string)
}

variable "private_route_table_ids" {
  description = "Route table IDs attached to private subnets (for S3 Gateway endpoint)"
  type        = list(string)
}

variable "endpoint_security_group_id" {
  description = "Security group ID attached to Interface Endpoints (allow inbound 443 from ECS SG)"
  type        = string
}

variable "create_s3_gateway_endpoint" {
  description = "Create S3 Gateway endpoint"
  type        = bool
  default     = true
}

variable "create_ecr_api_endpoint" {
  description = "Create Interface endpoint for ECR API"
  type        = bool
  default     = true
}

variable "create_ecr_dkr_endpoint" {
  description = "Create Interface endpoint for ECR DKR"
  type        = bool
  default     = true
}

variable "create_logs_endpoint" {
  description = "Create Interface endpoint for CloudWatch Logs"
  type        = bool
  default     = true
}

variable "cloudwatch_log_groups_retention" {
  description = "Map of log group names and retention days to manage via Terraform"
  type        = map(number)
  default = {
    "/ecs/course-registration-be" = 14
    "/ecs/course-registration-fe" = 14
  }
}

variable "ecr_lifecycle_keep_last" {
  description = "How many latest images to keep in each ECR repository"
  type        = number
  default     = 10
}

variable "ecr_repository_names" {
  description = "ECR repositories to attach lifecycle policy"
  type        = list(string)
  default     = ["app-backend", "app-frontend"]
}

variable "common_tags" {
  description = "Common tags for all resources"
  type        = map(string)
  default = {
    Project = "course-registration"
    Managed = "terraform"
  }
}
