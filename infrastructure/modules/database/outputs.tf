output "skills_table_arn" {
  value = aws_dynamodb_table.skills.arn
}

output "projects_table_arn" {
  value = aws_dynamodb_table.projects.arn
}

output "adrs_table_arn" {
  value = aws_dynamodb_table.adrs.arn
}

output "versions_table_arn" {
  value = aws_dynamodb_table.versions.arn
}

output "certifications_table_arn" {
  value = aws_dynamodb_table.certifications.arn
}

output "site_config_table_arn" {
  value = aws_dynamodb_table.site_config.arn
}

output "skills_table_name" {
  value = aws_dynamodb_table.skills.name
}

output "projects_table_name" {
  value = aws_dynamodb_table.projects.name
}

output "adrs_table_name" {
  value = aws_dynamodb_table.adrs.name
}

output "versions_table_name" {
  value = aws_dynamodb_table.versions.name
}

output "certifications_table_name" {
  value = aws_dynamodb_table.certifications.name
}

output "site_config_table_name" {
  value = aws_dynamodb_table.site_config.name
}