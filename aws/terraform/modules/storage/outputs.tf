output "frontend_bucket_name" {
  value = aws_s3_bucket.frontend.id
}

output "frontend_bucket_arn" {
  value = aws_s3_bucket.frontend.arn
}

output "frontend_website_endpoint" {
  value = aws_s3_bucket_website_configuration.frontend.website_endpoint
}

output "waf_logs_bucket_name" {
  value = aws_s3_bucket.waf_logs.id
}

output "waf_logs_bucket_arn" {
  value = aws_s3_bucket.waf_logs.arn
}

output "firehose_delivery_stream_arn" {
  value = aws_kinesis_firehose_delivery_stream.waf.arn
}
