# Cognito User Pool
resource "aws_cognito_user_pool" "admin_pool" {
  name = "${var.name_prefix}-admin-pool"

  # User attributes
  alias_attributes = ["email"]
  
  # Password policy
  password_policy {
    minimum_length    = 8
    require_lowercase = true
    require_numbers   = true
    require_symbols   = true
    require_uppercase = true
  }

  # Account recovery
  account_recovery_setting {
    recovery_mechanism {
      name     = "verified_email"
      priority = 1
    }
  }

  # Email configuration
  email_configuration {
    email_sending_account = "COGNITO_DEFAULT"
  }

  # Auto-verified attributes
  auto_verified_attributes = ["email"]

  # User pool add-ons
  user_pool_add_ons {
    advanced_security_mode = "ENFORCED"
  }

  tags = {
    Environment = var.environment
    Project     = var.name_prefix
  }
}

# Cognito User Pool Client
resource "aws_cognito_user_pool_client" "admin_client" {
  name         = "${var.name_prefix}-admin-client"
  user_pool_id = aws_cognito_user_pool.admin_pool.id

  # Client settings
  generate_secret                      = false
  prevent_user_existence_errors        = "ENABLED"
  enable_token_revocation             = true
  enable_propagate_additional_user_context_data = false

  # Auth flows
  explicit_auth_flows = [
    "ALLOW_USER_SRP_AUTH",
    "ALLOW_REFRESH_TOKEN_AUTH"
  ]

  # Token validity
  access_token_validity  = 60    # 1 hour
  id_token_validity     = 60    # 1 hour
  refresh_token_validity = 30   # 30 days

  token_validity_units {
    access_token  = "minutes"
    id_token      = "minutes"
    refresh_token = "days"
  }

  # Callback URLs (for future use)
  callback_urls = [
    "http://localhost:5173/admin",
    "https://${var.admin_domain}/admin"
  ]

  logout_urls = [
    "http://localhost:5173",
    "https://${var.admin_domain}"
  ]

  # OAuth settings
  allowed_oauth_flows                  = ["code"]
  allowed_oauth_flows_user_pool_client = true
  allowed_oauth_scopes                 = ["email", "openid", "profile"]
  supported_identity_providers         = ["COGNITO"]
}

# Cognito User Pool Domain
resource "aws_cognito_user_pool_domain" "admin_domain" {
  domain       = "${var.name_prefix}-admin-${random_string.domain_suffix.result}"
  user_pool_id = aws_cognito_user_pool.admin_pool.id
}

# Random string for unique domain
resource "random_string" "domain_suffix" {
  length  = 8
  special = false
  upper   = false
}

# Create initial admin user
resource "aws_cognito_user" "admin_user" {
  user_pool_id = aws_cognito_user_pool.admin_pool.id
  username     = var.admin_email

  attributes = {
    email          = var.admin_email
    email_verified = "true"
  }

  temporary_password = var.admin_temp_password
  message_action     = "SUPPRESS" # Don't send welcome email
}