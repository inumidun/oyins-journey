output "s3_bucket_name" {
  value = aws_s3_bucket.frontend.bucket
}

output "s3_admin_bucket_name" {
  value = aws_s3_bucket.admin.bucket
}

output "cloudfront_frontend_url" {
  value = "https://${aws_cloudfront_distribution.frontend.domain_name}"
}

output "cloudfront_admin_url" {
  value = "https://${aws_cloudfront_distribution.admin.domain_name}"
}

output "cloudfront_frontend_id" {
  value = aws_cloudfront_distribution.frontend.id
}

output "cloudfront_admin_id" {
  value = aws_cloudfront_distribution.admin.id
}