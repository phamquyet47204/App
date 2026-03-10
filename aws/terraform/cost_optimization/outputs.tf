output "s3_gateway_endpoint_id" {
  description = "S3 Gateway endpoint ID"
  value       = try(aws_vpc_endpoint.s3_gateway[0].id, null)
}

output "interface_endpoint_ids" {
  description = "Interface endpoint IDs"
  value = {
    for k, v in aws_vpc_endpoint.interface : k => v.id
  }
}

output "managed_log_groups" {
  description = "CloudWatch log groups managed by Terraform"
  value       = keys(aws_cloudwatch_log_group.retention)
}

output "ecr_lifecycle_repositories" {
  description = "ECR repositories with lifecycle policy attached"
  value       = [for r in aws_ecr_lifecycle_policy.this : r.repository]
}
