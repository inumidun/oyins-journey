# Lambda Functions Module - Simplified
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

# Package skills function
data "archive_file" "skills" {
  type        = "zip"
  source_dir  = "${path.module}/codes/skills"
  output_path = "${path.module}/packages/skills.zip"
}

# CloudWatch Log Group
resource "aws_cloudwatch_log_group" "skills_logs" {
  name              = "/aws/lambda/${aws_lambda_function.skills.function_name}"
  retention_in_days = 14
}