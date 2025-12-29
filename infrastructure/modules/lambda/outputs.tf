output "skills_function_arn" {
  value = aws_lambda_function.skills.arn
}

output "skills_invoke_arn" {
  value = aws_lambda_function.skills.invoke_arn
}