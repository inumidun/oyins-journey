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
  region  = var.aws_region
  profile = "default"
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
  default     = "dev"
}

# Local values for environment-specific naming
locals {
  name_prefix = "${var.project_name}-${var.environment}"
}

# DynamoDB Tables
resource "aws_dynamodb_table" "skills" {
  name           = "${local.name_prefix}-skills"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "skill_id"

  attribute {
    name = "skill_id"
    type = "S"
  }

  attribute {
    name = "category"
    type = "S"
  }

  global_secondary_index {
    name     = "CategoryIndex"
    hash_key = "category"
    projection_type = "ALL"
  }

  tags = {
    Name = "${local.name_prefix} Skills"
    Environment = var.environment
  }
}

resource "aws_dynamodb_table" "projects" {
  name           = "${local.name_prefix}-projects"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "project_id"

  attribute {
    name = "project_id"
    type = "S"
  }

  tags = {
    Name = "${local.name_prefix} Projects"
    Environment = var.environment
  }
}

resource "aws_dynamodb_table" "adrs" {
  name           = "${local.name_prefix}-adrs"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "adr_id"

  attribute {
    name = "adr_id"
    type = "S"
  }

  tags = {
    Name = "${local.name_prefix} Architecture Decisions"
    Environment = var.environment
  }
}

resource "aws_dynamodb_table" "versions" {
  name           = "${local.name_prefix}-versions"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "version_id"

  attribute {
    name = "version_id"
    type = "S"
  }

  tags = {
    Name = "${local.name_prefix} Versions"
    Environment = var.environment
  }
}

# Certifications Table
resource "aws_dynamodb_table" "certifications" {
  name           = "${local.name_prefix}-certifications"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "cert_id"

  attribute {
    name = "cert_id"
    type = "S"
  }

  attribute {
    name = "provider"
    type = "S"
  }

  global_secondary_index {
    name     = "ProviderIndex"
    hash_key = "provider"
    projection_type = "ALL"
  }

  tags = {
    Name = "${local.name_prefix} Certifications"
    Environment = var.environment
  }
}

# S3 Bucket for Frontend
resource "aws_s3_bucket" "frontend" {
  bucket = "${local.name_prefix}-frontend-${random_string.bucket_suffix.result}"
  
  tags = {
    Name = "${local.name_prefix} Frontend"
    Environment = var.environment
  }
}

# S3 Bucket for Admin
resource "aws_s3_bucket" "admin" {
  bucket = "${local.name_prefix}-admin-${random_string.bucket_suffix.result}"
  
  tags = {
    Name = "${local.name_prefix} Admin"
    Environment = var.environment
  }
}

resource "random_string" "bucket_suffix" {
  length  = 8
  special = false
  upper   = false
}

resource "aws_s3_bucket_website_configuration" "frontend" {
  bucket = aws_s3_bucket.frontend.id

  index_document {
    suffix = "index.html"
  }
}

resource "aws_s3_bucket_website_configuration" "admin" {
  bucket = aws_s3_bucket.admin.id

  index_document {
    suffix = "index.html"
  }
}

resource "aws_s3_bucket_public_access_block" "frontend" {
  bucket = aws_s3_bucket.frontend.id

  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

resource "aws_s3_bucket_public_access_block" "admin" {
  bucket = aws_s3_bucket.admin.id

  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

resource "aws_s3_bucket_policy" "frontend" {
  bucket = aws_s3_bucket.frontend.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid       = "PublicReadGetObject"
        Effect    = "Allow"
        Principal = "*"
        Action    = "s3:GetObject"
        Resource  = "${aws_s3_bucket.frontend.arn}/*"
      }
    ]
  })
}

resource "aws_s3_bucket_policy" "admin" {
  bucket = aws_s3_bucket.admin.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid       = "PublicReadGetObject"
        Effect    = "Allow"
        Principal = "*"
        Action    = "s3:GetObject"
        Resource  = "${aws_s3_bucket.admin.arn}/*"
      }
    ]
  })
}

# API Gateway
resource "aws_api_gateway_rest_api" "lar_api" {
  name        = "${local.name_prefix}-api"
  description = "Oyin's Journey API - ${var.environment}"
  
  tags = {
    Name = "${local.name_prefix} API"
    Environment = var.environment
  }
}

# Lambda IAM Role
resource "aws_iam_role" "lambda_role" {
  name = "${local.name_prefix}-lambda-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
  
  tags = {
    Name = "${local.name_prefix} Lambda Role"
    Environment = var.environment
  }
}

resource "aws_iam_role_policy" "lambda_policy" {
  name = "${local.name_prefix}-lambda-policy"
  role = aws_iam_role.lambda_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = "arn:aws:logs:*:*:*"
      },
      {
        Effect = "Allow"
        Action = [
          "dynamodb:GetItem",
          "dynamodb:PutItem",
          "dynamodb:Query",
          "dynamodb:Scan"
        ]
        Resource = [
          aws_dynamodb_table.skills.arn,
          aws_dynamodb_table.projects.arn,
          aws_dynamodb_table.adrs.arn,
          aws_dynamodb_table.versions.arn,
          aws_dynamodb_table.certifications.arn,
          "${aws_dynamodb_table.skills.arn}/index/*",
          "${aws_dynamodb_table.certifications.arn}/index/*"
        ]
      }
    ]
  })
}

# Outputs
output "api_gateway_url" {
  value = aws_api_gateway_rest_api.lar_api.execution_arn
}

output "s3_bucket_name" {
  value = aws_s3_bucket.frontend.bucket
}

output "s3_website_url" {
  value = aws_s3_bucket_website_configuration.frontend.website_endpoint
}

output "s3_admin_bucket_name" {
  value = aws_s3_bucket.admin.bucket
}

output "s3_admin_website_url" {
  value = aws_s3_bucket_website_configuration.admin.website_endpoint
}