terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
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

# API Module
module "api" {
  source = "./modules/api"
  
  name_prefix = local.name_prefix
  environment = var.environment
  dynamodb_table_arns = [
    module.database.skills_table_arn,
    module.database.projects_table_arn,
    module.database.adrs_table_arn,
    module.database.versions_table_arn,
    module.database.certifications_table_arn
  ]
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