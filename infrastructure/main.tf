terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    archive = {
      source  = "hashicorp/archive"
      version = "~> 2.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# Variables
variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Project name"
  type        = string
  default     = "oyins-journey"
}

variable "environment" {
  description = "Environment (dev, test, prod)"
  type        = string
}

variable "admin_email" {
  description = "Admin user email for Cognito"
  type        = string
  default     = null
}

variable "admin_temp_password" {
  description = "Temporary password for admin user"
  type        = string
  sensitive   = true
  default     = null
}

variable "use_ssm_password" {
  description = "Use password from SSM Parameter Store instead of variable"
  type        = bool
  default     = true
}
  type        = bool
  default     = false
}

# Local values for environment-specific naming
locals {
  name_prefix = "${var.project_name}-${var.environment}"
}

# Database Module
module "database" {
  source = "./modules/database"
  
  name_prefix = local.name_prefix
  environment = var.environment
}

# Frontend Module
module "frontend" {
  source = "./modules/frontend"
  
  name_prefix = local.name_prefix
  environment = var.environment
}

# Lambda Module
module "lambda" {
  source = "./modules/lambda"
  
  name_prefix      = local.name_prefix
  environment      = var.environment
  lambda_role_arn  = module.api.lambda_role_arn
}

# Cognito Module
module "cognito" {
  source = "./modules/cognito"
  
  name_prefix          = local.name_prefix
  environment          = var.environment
  admin_email          = var.admin_email
  admin_temp_password  = var.admin_temp_password
  use_ssm_password     = var.use_ssm_password
}

# API Module
module "api" {
  source = "./modules/api"
  
  name_prefix           = local.name_prefix
  environment           = var.environment
  dynamodb_table_arns   = [
    module.database.skills_table_arn,
    module.database.projects_table_arn,
    module.database.adrs_table_arn,
    module.database.versions_table_arn,
    module.database.certifications_table_arn,
    module.database.site_config_table_arn
  ]
  
  # Cognito configuration
  cognito_user_pool_arn = module.cognito.user_pool_arn
  
  # All Lambda functions
  skills_invoke_arn           = module.lambda.skills_invoke_arn
  skills_function_name        = module.lambda.skills_function_name
  projects_invoke_arn         = module.lambda.projects_invoke_arn
  projects_function_name      = module.lambda.projects_function_name
  certifications_invoke_arn   = module.lambda.certifications_invoke_arn
  certifications_function_name = module.lambda.certifications_function_name
  site_config_invoke_arn      = module.lambda.site_config_invoke_arn
  site_config_function_name   = module.lambda.site_config_function_name
}

# Outputs
output "api_gateway_url" {
  value = module.api.api_gateway_url
}

output "s3_bucket_name" {
  value = module.frontend.s3_bucket_name
}

output "s3_admin_bucket_name" {
  value = module.frontend.s3_admin_bucket_name
}

output "cloudfront_frontend_url" {
  value = module.frontend.cloudfront_frontend_url
}

output "cloudfront_admin_url" {
  value = module.frontend.cloudfront_admin_url
}

output "cloudfront_frontend_id" {
  value = module.frontend.cloudfront_frontend_id
}

output "cloudfront_admin_id" {
  value = module.frontend.cloudfront_admin_id
}

output "cognito_user_pool_id" {
  value = module.cognito.user_pool_id
}

output "cognito_user_pool_client_id" {
  value = module.cognito.user_pool_client_id
}

output "cognito_domain_url" {
  value = module.cognito.cognito_domain_url
}