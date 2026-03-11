output "redis_endpoint" {
  value = aws_elasticache_cluster.redis.cache_nodes[0].address
}

output "redis_port" {
  value = aws_elasticache_cluster.redis.port
}

output "redis_cluster_id" {
  value = aws_elasticache_cluster.redis.cluster_id
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
