output "api_gateway_url" {
  value = aws_api_gateway_rest_api.main.execution_arn
}

output "api_gateway_id" {
  value = aws_api_gateway_rest_api.main.id
}

output "lambda_role_arn" {
  value = aws_iam_role.lambda_role.arn
}