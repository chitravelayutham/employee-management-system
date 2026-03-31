output "ec2_public_ip" {
  value = aws_instance.mongodb.public_ip
}

output "mongo_public_ip" {
  value = aws_eip.mongo_ip.public_ip
}

output "mongo_private_ip" {
  value = aws_instance.mongodb.private_ip
}

output "mongo_instance_id" {
  value = aws_instance.mongodb.id
}

output "frontend_s3_url" {
  value = aws_s3_bucket.frontend.bucket_regional_domain_name
}

output "cloudfront_url" {
  value = aws_cloudfront_distribution.frontend.domain_name
}

output "cloudfront_distribution_id" {
  value = aws_cloudfront_distribution.frontend.id
}

output "api_gateway_url" {
  value = aws_apigatewayv2_api.api.api_endpoint
}