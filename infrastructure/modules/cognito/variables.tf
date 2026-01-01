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
}

variable "admin_temp_password" {
  description = "Temporary password for admin user"
  type        = string
  sensitive   = true
}