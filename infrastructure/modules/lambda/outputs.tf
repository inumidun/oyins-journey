# Lambda Module Outputs

output "skills_invoke_arn" {
  value = aws_lambda_function.skills.invoke_arn
}

output "skills_function_name" {
  value = aws_lambda_function.skills.function_name
}

output "projects_invoke_arn" {
  value = aws_lambda_function.projects.invoke_arn
}

output "projects_function_name" {
  value = aws_lambda_function.projects.function_name
}

output "certifications_invoke_arn" {
  value = aws_lambda_function.certifications.invoke_arn
}

output "certifications_function_name" {
  value = aws_lambda_function.certifications.function_name
}

output "adrs_invoke_arn" {
  value = aws_lambda_function.adrs.invoke_arn
}

output "adrs_function_name" {
  value = aws_lambda_function.adrs.function_name
}

output "health_invoke_arn" {
  value = aws_lambda_function.health.invoke_arn
}

output "health_function_name" {
  value = aws_lambda_function.health.function_name
}

output "evidence_linker_invoke_arn" {
  value = aws_lambda_function.evidence_linker.invoke_arn
}

output "evidence_linker_function_name" {
  value = aws_lambda_function.evidence_linker.function_name
}

output "site_config_invoke_arn" {
  value = aws_lambda_function.site_config.invoke_arn
}

output "site_config_function_name" {
  value = aws_lambda_function.site_config.function_name
}