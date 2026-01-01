output "user_pool_id" {
  description = "Cognito User Pool ID"
  value       = aws_cognito_user_pool.admin_pool.id
}

output "user_pool_client_id" {
  description = "Cognito User Pool Client ID"
  value       = aws_cognito_user_pool_client.admin_client.id
}

output "user_pool_domain" {
  description = "Cognito User Pool Domain"
  value       = aws_cognito_user_pool_domain.admin_domain.domain
}

output "user_pool_arn" {
  description = "Cognito User Pool ARN"
  value       = aws_cognito_user_pool.admin_pool.arn
}

output "cognito_domain_url" {
  description = "Cognito hosted UI domain URL"
  value       = "https://${aws_cognito_user_pool_domain.admin_domain.domain}.auth.${data.aws_region.current.name}.amazoncognito.com"
}

data "aws_region" "current" {}