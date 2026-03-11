output "redis_endpoint" {
  value       = aws_elasticache_replication_group.redis.primary_endpoint_address
  description = "Redis primary endpoint (write)"
}

output "redis_reader_endpoint" {
  value       = aws_elasticache_replication_group.redis.reader_endpoint_address
  description = "Redis reader endpoint (read, Multi-AZ load balanced)"
}

output "redis_port" {
  value = aws_elasticache_replication_group.redis.port
}

output "redis_cluster_id" {
  value = aws_elasticache_replication_group.redis.id
}

output "dynamodb_tables" {
  value = concat(
    [aws_dynamodb_table.accounts_user.name],
    [aws_dynamodb_table.courses_course.name],
    [aws_dynamodb_table.courses_registration.name],
    [aws_dynamodb_table.courses_registrationwindow.name],
    [aws_dynamodb_table.authtoken_token.name],
    [for t in aws_dynamodb_table.generic : t.name]
  )
}
