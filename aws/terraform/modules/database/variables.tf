variable "project" {
  type        = string
  description = "Project name"
}

variable "private_subnet_ids" {
  type        = list(string)
  description = "Private subnet IDs"
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

variable "redis_num_nodes" {
  type        = number
  default     = 2
  description = "Number of Redis nodes"
}
