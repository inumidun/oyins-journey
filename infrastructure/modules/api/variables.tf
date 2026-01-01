variable "name_prefix" {
  description = "Name prefix for resources"
  type        = string
}

variable "environment" {
  description = "Environment name"
  type        = string
}

variable "dynamodb_table_arns" {
  description = "List of DynamoDB table ARNs for Lambda permissions"
  type        = list(string)
}

variable "skills_invoke_arn" {
  description = "Skills Lambda function invoke ARN"
  type        = string
}

variable "skills_function_name" {
  description = "Skills Lambda function name"
  type        = string
}

variable "projects_invoke_arn" {
  description = "Projects Lambda function invoke ARN"
  type        = string
}

variable "projects_function_name" {
  description = "Projects Lambda function name"
  type        = string
}

variable "certifications_invoke_arn" {
  description = "Certifications Lambda function invoke ARN"
  type        = string
}

variable "certifications_function_name" {
  description = "Certifications Lambda function name"
  type        = string
}

variable "site_config_invoke_arn" {
  description = "Site Config Lambda function invoke ARN"
  type        = string
}

variable "site_config_function_name" {
  description = "Site Config Lambda function name"
  type        = string
}

variable "cognito_user_pool_arn" {
  description = "Cognito User Pool ARN for API authorization"
  type        = string
}