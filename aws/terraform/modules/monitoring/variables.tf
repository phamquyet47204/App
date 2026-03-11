variable "project" {
  type        = string
  description = "Project name"
}

variable "region" {
  type        = string
  description = "AWS region"
}

variable "account_id" {
  type        = string
  description = "AWS account ID"
}

variable "ecs_cluster_name" {
  type        = string
  description = "ECS cluster name"
}

variable "load_balancer_name" {
  type        = string
  description = "Load balancer name"
}

variable "environment" {
  type        = string
  default     = "production"
  description = "Environment name"
}
