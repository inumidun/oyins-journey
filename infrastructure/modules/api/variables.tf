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