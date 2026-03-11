data "aws_caller_identity" "current" {}

data "aws_region" "current" {}

# Networking Module
module "networking" {
  source = "./modules/networking"

  project                = var.project
  vpc_cidr              = var.vpc_cidr
  public_subnet_cidrs   = var.public_subnet_cidrs
  private_subnet_cidrs  = var.private_subnet_cidrs
  alb_security_group_id = module.security.alb_security_group_id
}

# Security Module
module "security" {
  source = "./modules/security"

  project            = var.project
  vpc_id             = module.networking.vpc_id
  domain_name        = var.domain_name
  region             = var.aws_region
  account_id         = data.aws_caller_identity.current.account_id
}

# Compute Module (ECS, Fargate)
module "compute" {
  source = "./modules/compute"

  project                      = var.project
  region                       = var.aws_region
  account_id                   = data.aws_caller_identity.current.account_id
  private_subnet_ids           = module.networking.private_subnet_ids
  ecs_security_group_id        = module.security.ecs_security_group_id
  target_group_arn             = module.networking.target_group_arn
  ecs_task_execution_role_arn  = module.security.ecs_task_execution_role_arn
  ecs_task_role_arn            = module.security.ecs_task_role_arn
  task_cpu                     = var.task_cpu
  task_memory                  = var.task_memory
  desired_count                = var.desired_count
  min_capacity                 = var.min_capacity
  max_capacity                 = var.max_capacity
  target_cpu_utilization       = var.target_cpu_utilization
  target_memory_utilization    = var.target_memory_utilization
  log_retention_days           = var.log_retention_days
  secrets_manager_name         = var.secrets_manager_name
}

# Database Module (DynamoDB, Redis)
module "database" {
  source = "./modules/database"

  project                       = var.project
  region                        = var.aws_region
  private_subnet_ids            = module.networking.private_subnet_ids
  elasticache_security_group_id = module.security.elasticache_security_group_id
  redis_node_type               = var.redis_node_type
}

# Storage Module (S3, Firehose)
module "storage" {
  source = "./modules/storage"

  project        = var.project
  account_id     = data.aws_caller_identity.current.account_id
  replica_region = var.replica_region

  providers = {
    aws         = aws
    aws.replica = aws.replica
  }
}

# Monitoring Module (CloudWatch, CloudTrail)
module "monitoring" {
  source = "./modules/monitoring"

  project              = var.project
  region               = var.aws_region
  account_id           = data.aws_caller_identity.current.account_id
  ecs_cluster_name     = module.compute.ecs_cluster_name
  load_balancer_name   = module.networking.alb_id
  environment          = var.environment
}

# CloudFront Distribution
resource "aws_cloudfront_distribution" "frontend" {
  origin {
    domain_name = module.storage.frontend_website_endpoint
    origin_id   = "S3Frontend"

    custom_origin_config {
      http_port              = 80
      https_port             = 443
      origin_protocol_policy = "http-only"
      origin_ssl_protocols   = ["TLSv1.2"]
    }
  }

  origin {
    domain_name = module.networking.alb_dns_name
    origin_id   = "ALBBackend"

    custom_origin_config {
      http_port              = 80
      https_port             = 443
      origin_protocol_policy = "http-only"
      origin_ssl_protocols   = ["TLSv1.2"]
    }
  }

  enabled             = true
  is_ipv6_enabled     = true
  default_root_object = "index.html"
  web_acl_id          = module.security.cloudfront_waf_arn

  default_cache_behavior {
    allowed_methods  = ["GET", "HEAD", "OPTIONS"]
    cached_methods   = ["GET", "HEAD"]
    target_origin_id = "S3Frontend"

    forwarded_values {
      query_string = false

      cookies {
        forward = "none"
      }
    }

    viewer_protocol_policy = "redirect-to-https"
    min_ttl                = 0
    default_ttl            = 3600
    max_ttl                = 86400
  }

  # API endpoints routed to ALB
  ordered_cache_behavior {
    path_pattern     = "/api/*"
    allowed_methods  = ["GET", "HEAD", "OPTIONS", "PUT", "POST", "PATCH", "DELETE"]
    cached_methods   = ["GET", "HEAD"]
    target_origin_id = "ALBBackend"

    forwarded_values {
      query_string = true

      cookies {
        forward = "all"
      }

      headers = ["*"]
    }

    viewer_protocol_policy = "redirect-to-https"
    min_ttl                = 0
    default_ttl            = 0
    max_ttl                = 0
  }

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  viewer_certificate {
    acm_certificate_arn      = module.security.acm_certificate_arn
    ssl_support_method       = "sni-only"
    minimum_protocol_version = "TLSv1.2_2021"
  }

  logging_config {
    include_cookies = false
    bucket          = module.storage.waf_logs_bucket_name
    prefix          = "cloudfront-logs/"
  }

  tags = {
    Name = "${var.project}-cloudfront"
  }
}

# Associate WAF with ALB
resource "aws_wafv2_web_acl_association" "alb" {
  resource_arn = module.networking.alb_arn
  web_acl_arn  = module.security.alb_waf_arn
}
