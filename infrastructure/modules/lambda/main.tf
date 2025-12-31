# Lambda Functions Module - Complete

# Skills Function
resource "aws_lambda_function" "skills" {
  filename         = "${path.module}/packages/skills.zip"
  function_name    = "${var.name_prefix}-skills"
  role            = var.lambda_role_arn
  handler         = "skills.lambda_handler"
  runtime         = "python3.13"
  timeout         = 30
  memory_size     = 256
  
  environment {
    variables = {
      SKILLS_TABLE = "${var.name_prefix}-skills"
      LOG_LEVEL    = "INFO"
      ENVIRONMENT  = var.environment
    }
  }
  
  depends_on = [data.archive_file.skills]
}

# Projects Function
resource "aws_lambda_function" "projects" {
  filename         = "${path.module}/packages/projects.zip"
  function_name    = "${var.name_prefix}-projects"
  role            = var.lambda_role_arn
  handler         = "projects.lambda_handler"
  runtime         = "python3.13"
  timeout         = 30
  memory_size     = 256
  
  environment {
    variables = {
      PROJECTS_TABLE = "${var.name_prefix}-projects"
      LOG_LEVEL      = "INFO"
      ENVIRONMENT    = var.environment
      GITHUB_TOKEN   = var.github_token
    }
  }
  
  depends_on = [data.archive_file.projects]
}

# Certifications Function
resource "aws_lambda_function" "certifications" {
  filename         = "${path.module}/packages/certifications.zip"
  function_name    = "${var.name_prefix}-certifications"
  role            = var.lambda_role_arn
  handler         = "certifications.lambda_handler"
  runtime         = "python3.13"
  timeout         = 30
  memory_size     = 256
  
  environment {
    variables = {
      CERTIFICATIONS_TABLE = "${var.name_prefix}-certifications"
      LOG_LEVEL           = "INFO"
      ENVIRONMENT         = var.environment
    }
  }
  
  depends_on = [data.archive_file.certifications]
}

# ADRs Function
resource "aws_lambda_function" "adrs" {
  filename         = "${path.module}/packages/adrs.zip"
  function_name    = "${var.name_prefix}-adrs"
  role            = var.lambda_role_arn
  handler         = "adrs.lambda_handler"
  runtime         = "python3.13"
  timeout         = 30
  memory_size     = 256
  
  environment {
    variables = {
      ADRS_TABLE  = "${var.name_prefix}-adrs"
      LOG_LEVEL   = "INFO"
      ENVIRONMENT = var.environment
    }
  }
  
  depends_on = [data.archive_file.adrs]
}

# Health Function
resource "aws_lambda_function" "health" {
  filename         = "${path.module}/packages/health.zip"
  function_name    = "${var.name_prefix}-health"
  role            = var.lambda_role_arn
  handler         = "health.lambda_handler"
  runtime         = "python3.13"
  timeout         = 30
  memory_size     = 256
  
  environment {
    variables = {
      SKILLS_TABLE         = "${var.name_prefix}-skills"
      PROJECTS_TABLE       = "${var.name_prefix}-projects"
      CERTIFICATIONS_TABLE = "${var.name_prefix}-certifications"
      ADRS_TABLE          = "${var.name_prefix}-adrs"
      API_GATEWAY_ID      = var.api_gateway_id
      SYSTEM_VERSION      = "2.1.0"
      ENVIRONMENT         = var.environment
      LOG_LEVEL           = "INFO"
    }
  }
  
  depends_on = [data.archive_file.health]
}

# Evidence Linker Function
resource "aws_lambda_function" "evidence_linker" {
  filename         = "${path.module}/packages/evidence_linker.zip"
  function_name    = "${var.name_prefix}-evidence-linker"
  role            = var.lambda_role_arn
  handler         = "evidence_linker.lambda_handler"
  runtime         = "python3.13"
  timeout         = 60  # Longer timeout for external API calls
  memory_size     = 512
  
  environment {
    variables = {
      SKILLS_TABLE         = "${var.name_prefix}-skills"
      PROJECTS_TABLE       = "${var.name_prefix}-projects"
      CERTIFICATIONS_TABLE = "${var.name_prefix}-certifications"
      GITHUB_TOKEN         = var.github_token
      LOG_LEVEL           = "INFO"
      ENVIRONMENT         = var.environment
    }
  }
  
  depends_on = [data.archive_file.evidence_linker]
}

# Package Functions
data "archive_file" "skills" {
  type        = "zip"
  source_dir  = "${path.module}/codes/skills"
  output_path = "${path.module}/packages/skills.zip"
}

data "archive_file" "projects" {
  type        = "zip"
  source_dir  = "${path.module}/codes/projects"
  output_path = "${path.module}/packages/projects.zip"
}

data "archive_file" "certifications" {
  type        = "zip"
  source_dir  = "${path.module}/codes/certifications"
  output_path = "${path.module}/packages/certifications.zip"
}

data "archive_file" "adrs" {
  type        = "zip"
  source_dir  = "${path.module}/codes/adrs"
  output_path = "${path.module}/packages/adrs.zip"
}

data "archive_file" "health" {
  type        = "zip"
  source_dir  = "${path.module}/codes/health"
  output_path = "${path.module}/packages/health.zip"
}

data "archive_file" "evidence_linker" {
  type        = "zip"
  source_dir  = "${path.module}/codes/evidence_linker"
  output_path = "${path.module}/packages/evidence_linker.zip"
}

# CloudWatch Log Groups
resource "aws_cloudwatch_log_group" "skills_logs" {
  name              = "/aws/lambda/${aws_lambda_function.skills.function_name}"
  retention_in_days = 14
}

resource "aws_cloudwatch_log_group" "projects_logs" {
  name              = "/aws/lambda/${aws_lambda_function.projects.function_name}"
  retention_in_days = 14
}

resource "aws_cloudwatch_log_group" "certifications_logs" {
  name              = "/aws/lambda/${aws_lambda_function.certifications.function_name}"
  retention_in_days = 14
}

resource "aws_cloudwatch_log_group" "adrs_logs" {
  name              = "/aws/lambda/${aws_lambda_function.adrs.function_name}"
  retention_in_days = 14
}

resource "aws_cloudwatch_log_group" "health_logs" {
  name              = "/aws/lambda/${aws_lambda_function.health.function_name}"
  retention_in_days = 14
}

resource "aws_cloudwatch_log_group" "evidence_linker_logs" {
  name              = "/aws/lambda/${aws_lambda_function.evidence_linker.function_name}"
  retention_in_days = 14
}