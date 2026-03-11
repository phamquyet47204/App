terraform {
  required_providers {
    aws = {
      source                = "hashicorp/aws"
      version               = "~> 5.0"
      configuration_aliases = [aws.replica]
    }
  }
}

variable "project" {
  type        = string
  description = "Project name"
}

variable "account_id" {
  type        = string
  description = "AWS account ID"
}

variable "replica_region" {
  type        = string
  default     = "ap-northeast-1"
  description = "Secondary region for S3 Cross-Region Replication (disaster recovery)"
}
