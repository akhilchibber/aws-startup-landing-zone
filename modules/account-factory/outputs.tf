output "account_id" {
  description = "AWS Account ID created for the team"
  value       = aws_organizations_account.team_account.id
}

output "account_arn" {
  description = "ARN of the created account"
  value       = aws_organizations_account.team_account.arn
}

output "account_status" {
  description = "Status of the created account"
  value       = aws_organizations_account.team_account.status
}

output "cross_account_role_arn" {
  description = "ARN of cross-account access role"
  value       = aws_iam_role.team_account_access.arn
}

output "team_name" {
  description = "Team name"
  value       = var.team_name
}

output "team_email" {
  description = "Team email"
  value       = var.team_email
}

output "cost_center" {
  description = "Cost center code"
  value       = var.cost_center
}

output "account_info_parameter" {
  description = "SSM Parameter containing account information"
  value       = aws_ssm_parameter.account_info.name
}
