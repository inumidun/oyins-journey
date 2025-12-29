output "skills_function_arn" {
  value = aws_lambda_function.skills.arn
}

output "skills_invoke_arn" {
  value = aws_lambda_function.skills.invoke_arn
}

output "projects_function_arn" {
  value = aws_lambda_function.projects.arn
}

output "projects_invoke_arn" {
  value = aws_lambda_function.projects.invoke_arn
}

output "certifications_function_arn" {
  value = aws_lambda_function.certifications.arn
}

output "certifications_invoke_arn" {
  value = aws_lambda_function.certifications.invoke_arn
}

output "adrs_function_arn" {
  value = aws_lambda_function.adrs.arn
}

output "adrs_invoke_arn" {
  value = aws_lambda_function.adrs.invoke_arn
}

output "version_function_arn" {
  value = aws_lambda_function.version.arn
}

output "version_invoke_arn" {
  value = aws_lambda_function.version.invoke_arn
}