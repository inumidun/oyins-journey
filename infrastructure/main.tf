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

# S3 Bucket for Frontend (Private)
resource "aws_s3_bucket" "frontend" {
  bucket = "${local.name_prefix}-frontend-${random_string.bucket_suffix.result}"
  
  tags = {
    Name = "${local.name_prefix} Frontend"
    Environment = var.environment
  }
}

# S3 Bucket for Admin (Private)
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

# CloudFront Origin Access Control
resource "aws_cloudfront_origin_access_control" "frontend" {
  name                              = "${local.name_prefix}-frontend-oac"
  description                       = "OAC for ${local.name_prefix} frontend"
  origin_access_control_origin_type = "s3"
  signing_behavior                  = "always"
  signing_protocol                  = "sigv4"
}

resource "aws_cloudfront_origin_access_control" "admin" {
  name                              = "${local.name_prefix}-admin-oac"
  description                       = "OAC for ${local.name_prefix} admin"
  origin_access_control_origin_type = "s3"
  signing_behavior                  = "always"
  signing_protocol                  = "sigv4"
}

# CloudFront Distribution for Frontend
resource "aws_cloudfront_distribution" "frontend" {
  origin {
    domain_name              = aws_s3_bucket.frontend.bucket_regional_domain_name
    origin_access_control_id = aws_cloudfront_origin_access_control.frontend.id
    origin_id                = "S3-${aws_s3_bucket.frontend.bucket}"
  }

  enabled             = true
  default_root_object = "index.html"

  default_cache_behavior {
    allowed_methods        = ["DELETE", "GET", "HEAD", "OPTIONS", "PATCH", "POST", "PUT"]
    cached_methods         = ["GET", "HEAD"]
    target_origin_id       = "S3-${aws_s3_bucket.frontend.bucket}"
    compress               = true
    viewer_protocol_policy = "redirect-to-https"

    forwarded_values {
      query_string = false
      cookies {
        forward = "none"
      }
    }
  }

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  viewer_certificate {
    cloudfront_default_certificate = true
  }

  tags = {
    Name = "${local.name_prefix} Frontend CDN"
    Environment = var.environment
  }
}

# CloudFront Distribution for Admin
resource "aws_cloudfront_distribution" "admin" {
  origin {
    domain_name              = aws_s3_bucket.admin.bucket_regional_domain_name
    origin_access_control_id = aws_cloudfront_origin_access_control.admin.id
    origin_id                = "S3-${aws_s3_bucket.admin.bucket}"
  }

  enabled             = true
  default_root_object = "index.html"

  default_cache_behavior {
    allowed_methods        = ["DELETE", "GET", "HEAD", "OPTIONS", "PATCH", "POST", "PUT"]
    cached_methods         = ["GET", "HEAD"]
    target_origin_id       = "S3-${aws_s3_bucket.admin.bucket}"
    compress               = true
    viewer_protocol_policy = "redirect-to-https"

    forwarded_values {
      query_string = false
      cookies {
        forward = "none"
      }
    }
  }

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  viewer_certificate {
    cloudfront_default_certificate = true
  }

  tags = {
    Name = "${local.name_prefix} Admin CDN"
    Environment = var.environment
  }
}

# S3 Bucket Policy for CloudFront OAC
resource "aws_s3_bucket_policy" "frontend" {
  bucket = aws_s3_bucket.frontend.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "AllowCloudFrontServicePrincipal"
        Effect = "Allow"
        Principal = {
          Service = "cloudfront.amazonaws.com"
        }
        Action   = "s3:GetObject"
        Resource = "${aws_s3_bucket.frontend.arn}/*"
        Condition = {
          StringEquals = {
            "AWS:SourceArn" = aws_cloudfront_distribution.frontend.arn
          }
        }
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
        Sid    = "AllowCloudFrontServicePrincipal"
        Effect = "Allow"
        Principal = {
          Service = "cloudfront.amazonaws.com"
        }
        Action   = "s3:GetObject"
        Resource = "${aws_s3_bucket.admin.arn}/*"
        Condition = {
          StringEquals = {
            "AWS:SourceArn" = aws_cloudfront_distribution.admin.arn
          }
        }
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

output "s3_admin_bucket_name" {
  value = aws_s3_bucket.admin.bucket
}

output "cloudfront_frontend_url" {
  value = "https://${aws_cloudfront_distribution.frontend.domain_name}"
}

output "cloudfront_admin_url" {
  value = "https://${aws_cloudfront_distribution.admin.domain_name}"
}