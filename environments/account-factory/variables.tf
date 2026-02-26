# Account Factory Variables
# These are populated from the GitHub Actions workflow

variable "aws_region" {
  description = "AWS region for account factory"
  type        = string
  default     = "eu-north-1"
}

variable "organization_unit_id" {
  description = "AWS Organization Unit ID where account will be created"
  type        = string
  default     = ""  # Empty string means use root OU or skip if Organizations not enabled
}

# Team Information
variable "team_name" {
  description = "Name of the hospital team/department"
  type        = string
}

variable "team_lead" {
  description = "Primary contact for the account"
  type        = string
}

variable "team_email" {
  description = "Team email address for notifications"
  type        = string
}

variable "cost_center" {
  description = "Cost center code for billing"
  type        = string
}

# Data & Compliance
variable "data_classification" {
  description = "Data classification level"
  type        = string
}

variable "business_criticality" {
  description = "Business criticality level"
  type        = string
}

variable "primary_use_case" {
  description = "Primary use case for the account"
  type        = string
}

variable "compliance_requirements" {
  description = "Compliance requirements"
  type        = string
  default     = "HIPAA"
}

# Budget & Services
variable "monthly_budget" {
  description = "Estimated monthly budget in USD"
  type        = number
}

variable "additional_services" {
  description = "Additional AWS services needed"
  type        = string
  default     = ""
}

# VPC CIDR Blocks for each environment
variable "dev_vpc_cidr" {
  description = "CIDR block for dev environment VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "staging_vpc_cidr" {
  description = "CIDR block for staging environment VPC"
  type        = string
  default     = "10.1.0.0/16"
}

variable "prod_vpc_cidr" {
  description = "CIDR block for prod environment VPC"
  type        = string
  default     = "10.2.0.0/16"
}
