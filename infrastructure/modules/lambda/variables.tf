variable "name_prefix" {
  description = "Name prefix for resources"
  type        = string
}

variable "environment" {
  description = "Environment name"
  type        = string
}

variable "lambda_role_arn" {
  description = "ARN of the Lambda execution role"
  type        = string
}

variable "github_token" {
  description = "GitHub token for API access"
  type        = string
  default     = ""
  sensitive   = true
}

variable "api_gateway_id" {
  description = "API Gateway ID for health monitoring"
  type        = string
  default     = ""
}