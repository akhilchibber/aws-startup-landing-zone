# AWS Account Factory Module
# Creates new AWS accounts for hospital teams with proper organization structure

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# Create AWS account
resource "aws_organizations_account" "team_account" {
  name              = var.team_name
  email             = var.team_email
  parent_id         = var.organization_unit_id
  iam_user_access_to_billing = "ALLOW"
  
  tags = merge(
    var.common_tags,
    {
      Name        = var.team_name
      TeamLead    = var.team_lead
      CostCenter  = var.cost_center
      DataClass   = var.data_classification
      Criticality = var.business_criticality
      UseCase     = var.primary_use_case
      Budget      = var.monthly_budget
    }
  )
}

# Wait for account to be created
resource "time_sleep" "account_creation" {
  depends_on      = [aws_organizations_account.team_account]
  create_duration = "30s"
}

# Create IAM role for cross-account access in the master account
# This role allows the master account to manage the new account
resource "aws_iam_role" "team_account_access" {
  name = "${var.team_name}-cross-account-access"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          AWS = data.aws_caller_identity.current.account_id
        }
        Action = "sts:AssumeRole"
      }
    ]
  })

  tags = var.common_tags
}

# Get current account ID (master account)
data "aws_caller_identity" "current" {}

# Attach admin policy for team account
resource "aws_iam_role_policy_attachment" "team_account_admin" {
  role       = aws_iam_role.team_account_access.name
  policy_arn = "arn:aws:iam::aws:policy/AdministratorAccess"
}

# Create budget alert for cost control
resource "aws_budgets_budget" "team_budget" {
  name              = "${var.team_name}-monthly-budget"
  budget_type       = "COST"
  limit_unit        = "USD"
  limit_amount      = var.monthly_budget
  time_period_start = "2026-01-01_00:00"
  time_period_end   = "2050-12-31_23:59"
  time_unit         = "MONTHLY"

  cost_filter {
    name   = "TagKeyValue"
    values = ["CostCenter$${var.cost_center}"]
  }

  notification {
    comparison_operator = "GREATER_THAN"
    notification_type   = "FORECASTED"
    threshold           = 80
    threshold_type      = "PERCENTAGE"
    
    subscriber {
      subscription_type = "EMAIL"
      address          = var.team_email
    }
  }

  notification {
    comparison_operator = "GREATER_THAN"
    notification_type   = "ACTUAL"
    threshold           = 100
    threshold_type      = "PERCENTAGE"
    
    subscriber {
      subscription_type = "EMAIL"
      address          = var.team_email
    }
  }
}

# Store account details in SSM Parameter Store for reference
resource "aws_ssm_parameter" "account_info" {
  name  = "/hospital/accounts/${var.team_name}/info"
  type  = "String"
  value = jsonencode({
    account_id              = aws_organizations_account.team_account.id
    team_name               = var.team_name
    team_lead               = var.team_lead
    team_email              = var.team_email
    cost_center             = var.cost_center
    data_classification     = var.data_classification
    business_criticality    = var.business_criticality
    primary_use_case        = var.primary_use_case
    monthly_budget          = var.monthly_budget
    compliance_requirements = var.compliance_requirements
    created_at              = timestamp()
  })

  tags = var.common_tags
}
