locals {
  interface_endpoints = {
    ecr_api = {
      enabled      = var.create_ecr_api_endpoint
      service_name = "com.amazonaws.${var.aws_region}.ecr.api"
      name         = "vpce-ecr-api"
    }
    ecr_dkr = {
      enabled      = var.create_ecr_dkr_endpoint
      service_name = "com.amazonaws.${var.aws_region}.ecr.dkr"
      name         = "vpce-ecr-dkr"
    }
    logs = {
      enabled      = var.create_logs_endpoint
      service_name = "com.amazonaws.${var.aws_region}.logs"
      name         = "vpce-logs"
    }
  }

  lifecycle_policy = jsonencode({
    rules = [
      {
        rulePriority = 1
        description  = "Keep last ${var.ecr_lifecycle_keep_last} images"
        selection = {
          tagStatus   = "any"
          countType   = "imageCountMoreThan"
          countNumber = var.ecr_lifecycle_keep_last
        }
        action = {
          type = "expire"
        }
      }
    ]
  })
}

resource "aws_vpc_endpoint" "s3_gateway" {
  count = var.create_s3_gateway_endpoint ? 1 : 0

  vpc_id            = var.vpc_id
  service_name      = "com.amazonaws.${var.aws_region}.s3"
  vpc_endpoint_type = "Gateway"
  route_table_ids   = var.private_route_table_ids

  tags = merge(var.common_tags, {
    Name = "vpce-s3"
  })
}

resource "aws_vpc_endpoint" "interface" {
  for_each = {
    for k, v in local.interface_endpoints : k => v if v.enabled
  }

  vpc_id              = var.vpc_id
  service_name        = each.value.service_name
  vpc_endpoint_type   = "Interface"
  private_dns_enabled = true
  subnet_ids          = var.private_subnet_ids
  security_group_ids  = [var.endpoint_security_group_id]

  tags = merge(var.common_tags, {
    Name = each.value.name
  })
}

resource "aws_cloudwatch_log_group" "retention" {
  for_each = var.cloudwatch_log_groups_retention

  name              = each.key
  retention_in_days = each.value
  tags              = var.common_tags
}

resource "aws_ecr_lifecycle_policy" "this" {
  for_each = toset(var.ecr_repository_names)

  repository = each.value
  policy     = local.lifecycle_policy
}
