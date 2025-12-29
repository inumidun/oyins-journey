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
    }
  }
  
  depends_on = [data.archive_file.certifications]
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