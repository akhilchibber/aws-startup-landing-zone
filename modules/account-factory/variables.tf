variable "team_name" {
  description = "Name of the hospital team/department"
  type        = string
  
  validation {
    condition     = can(regex("^[a-z0-9-_]+$", var.team_name))
    error_message = "Team name must be lowercase alphanumeric with hyphens or underscores."
  }
}

variable "team_lead" {
  description = "Primary contact for the account"
  type        = string
}

variable "team_email" {
  description = "Team email address for notifications"
  type        = string
  
  validation {
    condition     = can(regex("^[a-zA-Z0-9._%+-]+@hospital\\.com$", var.team_email))
    error_message = "Team email must be a valid hospital domain (@hospital.com)."
  }
}

variable "cost_center" {
  description = "Cost center code for billing"
  type        = string
  
  validation {
    condition     = can(regex("^CC-[A-Z]+-[0-9]+$", var.cost_center))
    error_message = "Cost center must follow format CC-DEPARTMENT-XXX."
  }
}

variable "data_classification" {
  description = "Data classification level"
  type        = string
  
  validation {
    condition     = contains(["Public", "Internal", "Confidential", "Restricted"], var.data_classification)
    error_message = "Data classification must be one of: Public, Internal, Confidential, Restricted."
  }
}

variable "business_criticality" {
  description = "Business criticality level"
  type        = string
  
  validation {
    condition     = contains(["Low", "Medium", "High", "Critical"], var.business_criticality)
    error_message = "Business criticality must be one of: Low, Medium, High, Critical."
  }
}

variable "primary_use_case" {
  description = "Primary use case for the account"
  type        = string
}

variable "monthly_budget" {
  description = "Estimated monthly budget in USD"
  type        = number
  
  validation {
    condition     = var.monthly_budget >= 100 && var.monthly_budget <= 100000
    error_message = "Monthly budget must be between $100 and $100,000."
  }
}

variable "compliance_requirements" {
  description = "Compliance requirements (comma-separated)"
  type        = string
  default     = "HIPAA"
}

variable "additional_services" {
  description = "Additional AWS services needed"
  type        = string
  default     = ""
}

variable "organization_unit_id" {
  description = "AWS Organization Unit ID where account will be created"
  type        = string
}

variable "common_tags" {
  description = "Common tags to apply to all resources"
  type        = map(string)
  default = {
    Product     = "Hospital-Landing-Zone"
    Environment = "Account-Factory"
    Component   = "Account-Management"
    ManagedBy   = "Terraform"
  }
}
