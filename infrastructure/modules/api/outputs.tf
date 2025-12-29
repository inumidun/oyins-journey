output "api_gateway_url" {
  value = "https://${aws_api_gateway_rest_api.main.id}.execute-api.${data.aws_region.current.name}.amazonaws.com/${aws_api_gateway_deployment.main.stage_name}"
}

output "api_gateway_id" {
  value = aws_api_gateway_rest_api.main.id
}

output "lambda_role_arn" {
  value = aws_iam_role.lambda_role.arn
}

data "aws_region" "current" {}