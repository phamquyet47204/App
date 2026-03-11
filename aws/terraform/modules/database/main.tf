# DynamoDB Tables
locals {
  tables = [
    "accounts_user",
    "accounts_user_groups",
    "accounts_user_user_permissions",
    "auth_group",
    "auth_group_permissions",
    "auth_permission",
    "authtoken_token",
    "courses_course",
    "courses_registration",
    "courses_registrationwindow",
    "django_admin_log",
    "django_content_type",
    "django_migrations",
    "django_session"
  ]
}

# DynamoDB Table: accounts_user
resource "aws_dynamodb_table" "accounts_user" {
  name           = "accounts_user"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "id"

  attribute {
    name = "id"
    type = "N"
  }

  # GSIs for lookups
  global_secondary_index {
    name            = "username-index"
    hash_key        = "username"
    projection_type = "ALL"
  }

  global_secondary_index {
    name            = "email-index"
    hash_key        = "email"
    projection_type = "ALL"
  }

  global_secondary_index {
    name            = "mssv-index"
    hash_key        = "mssv"
    projection_type = "ALL"
  }

  attribute {
    name = "username"
    type = "S"
  }

  attribute {
    name = "email"
    type = "S"
  }

  attribute {
    name = "mssv"
    type = "S"
  }

  tags = {
    Name = "accounts_user"
  }
}

# DynamoDB Table: courses_course
resource "aws_dynamodb_table" "courses_course" {
  name           = "courses_course"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "id"

  attribute {
    name = "id"
    type = "N"
  }

  tags = {
    Name = "courses_course"
  }
}

# DynamoDB Table: courses_registration
resource "aws_dynamodb_table" "courses_registration" {
  name           = "courses_registration"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "id"

  attribute {
    name = "id"
    type = "N"
  }

  # GSI for lookup by student+course
  global_secondary_index {
    name            = "student_course-index"
    hash_key        = "student_id"
    range_key       = "course_id"
    projection_type = "ALL"
  }

  attribute {
    name = "student_id"
    type = "N"
  }

  attribute {
    name = "course_id"
    type = "N"
  }

  tags = {
    Name = "courses_registration"
  }
}

# DynamoDB Table: courses_registrationwindow
resource "aws_dynamodb_table" "courses_registrationwindow" {
  name           = "courses_registrationwindow"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "id"

  attribute {
    name = "id"
    type = "N"
  }

  tags = {
    Name = "courses_registrationwindow"
  }
}

# DynamoDB Table: authtoken_token
resource "aws_dynamodb_table" "authtoken_token" {
  name           = "authtoken_token"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "key"

  attribute {
    name = "key"
    type = "S"
  }

  # GSI for lookup by user_id
  global_secondary_index {
    name            = "user_id-index"
    hash_key        = "user_id"
    projection_type = "ALL"
  }

  attribute {
    name = "user_id"
    type = "N"
  }

  tags = {
    Name = "authtoken_token"
  }
}

# Generic tables
resource "aws_dynamodb_table" "generic" {
  for_each = toset([
    "accounts_user_groups",
    "accounts_user_user_permissions",
    "auth_group",
    "auth_group_permissions",
    "auth_permission",
    "django_admin_log",
    "django_content_type",
    "django_migrations",
    "django_session"
  ])

  name           = each.value
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "id"

  attribute {
    name = "id"
    type = "N"
  }

  tags = {
    Name = each.value
  }
}

# ElastiCache Redis Subnet Group
resource "aws_elasticache_subnet_group" "main" {
  name       = "${var.project}-redis-subnet-group"
  subnet_ids = var.private_subnet_ids

  tags = {
    Name = "${var.project}-redis-subnet-group"
  }
}

# ElastiCache Redis Cluster
resource "aws_elasticache_cluster" "redis" {
  cluster_id           = "${var.project}-redis"
  engine               = "redis"
  node_type           = var.redis_node_type
  num_cache_nodes     = var.redis_num_nodes
  parameter_group_name = "default.redis7"
  engine_version      = "7.0"
  port                = 6379
  subnet_group_name   = aws_elasticache_subnet_group.main.name
  security_group_ids  = [var.elasticache_security_group_id]

  # Note: ElastiCache cluster (non-replication-group) has limited features
  # For HA and encryption, use aws_elasticache_replication_group instead
  # automatic_failover_enabled = true
  # at_rest_encryption_enabled = true
  # transit_encryption_enabled = true

  log_delivery_configuration {
    destination      = aws_cloudwatch_log_group.redis_slow.name
    destination_type = "cloudwatch-logs"
    log_format       = "json"
    log_type         = "slow-log"
  }

  log_delivery_configuration {
    destination      = aws_cloudwatch_log_group.redis_engine.name
    destination_type = "cloudwatch-logs"
    log_format       = "json"
    log_type         = "engine-log"
  }

  tags = {
    Name = "${var.project}-redis"
  }

  depends_on = [
    aws_cloudwatch_log_group.redis_slow,
    aws_cloudwatch_log_group.redis_engine
  ]
}

# CloudWatch Log Groups for Redis
resource "aws_cloudwatch_log_group" "redis_slow" {
  name              = "/aws/elasticache/${var.project}/slow-log"
  retention_in_days = 7

  tags = {
    Name = "${var.project}-redis-slow-logs"
  }
}

resource "aws_cloudwatch_log_group" "redis_engine" {
  name              = "/aws/elasticache/${var.project}/engine-log"
  retention_in_days = 7

  tags = {
    Name = "${var.project}-redis-engine-logs"
  }
}
