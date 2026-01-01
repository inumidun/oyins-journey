variable "name_prefix" {
  description = "Name prefix for resources"
  type        = string
}

variable "environment" {
  description = "Environment (dev, test, prod)"
  type        = string
}

variable "admin_domain" {
  description = "Admin portal domain"
  type        = string
  default     = "localhost:5173"
}

variable "admin_email" {
  description = "Admin user email"
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
  description = "Use credentials from SSM Parameter Store instead of variables"
  type        = bool
  default     = true
}