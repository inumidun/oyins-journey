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

# DynamoDB Tables
resource "aws_dynamodb_table" "skills" {
  name           = "${var.project_name}-skills"
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
    Name = "LAR Skills"
  }
}

resource "aws_dynamodb_table" "projects" {
  name           = "${var.project_name}-projects"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "project_id"

  attribute {
    name = "project_id"
    type = "S"
  }

  tags = {
    Name = "LAR Projects"
  }
}

resource "aws_dynamodb_table" "adrs" {
  name           = "${var.project_name}-adrs"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "adr_id"

  attribute {
    name = "adr_id"
    type = "S"
  }

  tags = {
    Name = "LAR Architecture Decisions"
  }
}

resource "aws_dynamodb_table" "versions" {
  name           = "${var.project_name}-versions"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "version_id"

  attribute {
    name = "version_id"
    type = "S"
  }

  tags = {
    Name = "Oyins Journey Versions"
  }
}

# Certifications Table
resource "aws_dynamodb_table" "certifications" {
  name           = "${var.project_name}-certifications"
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
    Name = "Oyins Journey Certifications"
  }
}

# S3 Bucket for Frontend
resource "aws_s3_bucket" "frontend" {
  bucket = "${var.project_name}-frontend-${random_string.bucket_suffix.result}"
}

# S3 Bucket for Admin
resource "aws_s3_bucket" "admin" {
  bucket = "${var.project_name}-admin-${random_string.bucket_suffix.result}"
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
  name        = "${var.project_name}-api"
  description = "Oyin's Journey API"
}

# Lambda IAM Role
resource "aws_iam_role" "lambda_role" {
  name = "${var.project_name}-lambda-role"

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
}

resource "aws_iam_role_policy" "lambda_policy" {
  name = "${var.project_name}-lambda-policy"
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