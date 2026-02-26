# Account Factory Outputs
# These are used by GitHub Actions to provide feedback to the team

output "account_id" {
  description = "AWS Account ID created for the team"
  value       = module.account_factory.account_id
}

output "account_arn" {
  description = "ARN of the created account"
  value       = module.account_factory.account_arn
}

output "team_name" {
  description = "Team name"
  value       = module.account_factory.team_name
}

output "team_email" {
  description = "Team email"
  value       = module.account_factory.team_email
}

output "cost_center" {
  description = "Cost center code"
  value       = module.account_factory.cost_center
}

# Dev Environment Outputs
output "dev_vpc_id" {
  description = "Dev environment VPC ID"
  value       = module.dev_environment.vpc_id
}

output "dev_public_subnets" {
  description = "Dev environment public subnet IDs"
  value       = module.dev_environment.public_subnet_ids
}

output "dev_private_subnets" {
  description = "Dev environment private subnet IDs"
  value       = module.dev_environment.private_subnet_ids
}

# For backward compatibility with workflow
output "dev_account_id" {
  description = "Dev account ID (same as main account for testing)"
  value       = module.account_factory.account_id
}

output "staging_account_id" {
  description = "Staging account ID (same as main account for testing)"
  value       = module.account_factory.account_id
}

output "prod_account_id" {
  description = "Prod account ID (same as main account for testing)"
  value       = module.account_factory.account_id
}

# Summary Output
output "provisioning_summary" {
  description = "Summary of provisioned resources"
  value = {
    account_id              = module.account_factory.account_id
    team_name               = module.account_factory.team_name
    team_email              = module.account_factory.team_email
    cost_center             = module.account_factory.cost_center
    dev_vpc_id              = module.dev_environment.vpc_id
    provisioning_status     = "Complete"
    provisioning_timestamp  = timestamp()
  }
}
