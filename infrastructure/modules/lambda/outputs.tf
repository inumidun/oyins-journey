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