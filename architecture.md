Student
   |
 HTTPS
   v
Route 53
   |
   v
CloudFront + WAF(Https only)
   |
   +----------------------------+
   |                            |
   |                            v
   |                     ALB (HTTPS + ACM + WAF)
   |                            |
   |                            v
   |                     Backend ECS Fargate   <--------------  ECR    <--------- Dev,...
   |                            |
   |         +------------------+------------------+
   |         |                  |                  |
   |         v                  v                  v
   |   Secrets Manager   ElastiCache Redis <=>   DynamoDB
   |                                               |
   |                                               v
   |                                            Lambda
   |                                               |
   |                                               v
   |                                              SES
   |
   v
S3 Static Website Bucket
   |
   v
HTML / CSS / JS / Images

Monitoring & Logging
- CloudWatch Metrics
- CloudWatch Logs
- CloudWatch Dashboard
- X-Ray
- CloudTrail
- WAF logs - firehoue -> S3