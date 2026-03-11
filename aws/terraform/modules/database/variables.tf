variable "project" {
  type        = string
  description = "Project name"
}

variable "region" {
  type        = string
  default     = "ap-southeast-1"
  description = "Primary AWS region"
}

variable "private_subnet_ids" {
  type        = list(string)
  description = "Private subnet IDs (must span at least 2 AZs for Multi-AZ Redis)"
}

variable "elasticache_security_group_id" {
  type        = string
  description = "ElastiCache security group ID"
}

variable "redis_node_type" {
  type        = string
  default     = "cache.t3.micro"
  description = "Redis node type"
}
