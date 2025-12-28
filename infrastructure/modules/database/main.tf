# DynamoDB Tables
resource "aws_dynamodb_table" "skills" {
  name           = "${var.name_prefix}-skills"
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
    Name = "${var.name_prefix} Skills"
    Environment = var.environment
  }
}

resource "aws_dynamodb_table" "projects" {
  name           = "${var.name_prefix}-projects"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "project_id"

  attribute {
    name = "project_id"
    type = "S"
  }

  tags = {
    Name = "${var.name_prefix} Projects"
    Environment = var.environment
  }
}

resource "aws_dynamodb_table" "adrs" {
  name           = "${var.name_prefix}-adrs"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "adr_id"

  attribute {
    name = "adr_id"
    type = "S"
  }

  tags = {
    Name = "${var.name_prefix} Architecture Decisions"
    Environment = var.environment
  }
}

resource "aws_dynamodb_table" "versions" {
  name           = "${var.name_prefix}-versions"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "version_id"

  attribute {
    name = "version_id"
    type = "S"
  }

  tags = {
    Name = "${var.name_prefix} Versions"
    Environment = var.environment
  }
}

resource "aws_dynamodb_table" "certifications" {
  name           = "${var.name_prefix}-certifications"
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
    Name = "${var.name_prefix} Certifications"
    Environment = var.environment
  }
}