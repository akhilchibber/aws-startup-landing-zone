terraform {
  required_version = ">= 1.0"
  
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  backend "s3" {
    # Backend config provided via CLI flags during init
    # bucket         = "hospital-terraform-state"
    # key            = "account-factory/state"
    # region         = "eu-north-1"
    # dynamodb_table = "terraform-locks"
    # encrypt        = true
  }
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Product     = "Hospital-Landing-Zone"
      Environment = "Account-Factory"
      Component   = "Account-Management"
      ManagedBy   = "Terraform"
      CreatedBy   = "GitHub-Actions"
    }
  }
}

# Create AWS account for the team
module "account_factory" {
  source = "../../modules/account-factory"

  team_name                = var.team_name
  team_lead                = var.team_lead
  team_email               = var.team_email
  cost_center              = var.cost_center
  data_classification      = var.data_classification
  business_criticality     = var.business_criticality
  primary_use_case         = var.primary_use_case
  monthly_budget           = var.monthly_budget
  compliance_requirements  = var.compliance_requirements
  additional_services      = var.additional_services
  organization_unit_id     = var.organization_unit_id

  common_tags = {
    Product     = "Hospital-Landing-Zone"
    Environment = "Account-Factory"
    Component   = "Account-Management"
    ManagedBy   = "Terraform"
    CreatedBy   = "GitHub-Actions"
    TeamName    = var.team_name
    CostCenter  = var.cost_center
  }
}

# Create dev environment in the new account
module "dev_environment" {
  source = "../../modules/environment"
  
  providers = {
    aws = aws.team_account_dev
  }

  team_name   = var.team_name
  environment = "dev"
  vpc_cidr    = var.dev_vpc_cidr

  common_tags = {
    Product     = "Hospital-Landing-Zone"
    Environment = "dev"
    Component   = "Landing-Zone"
    ManagedBy   = "Terraform"
    CreatedBy   = "GitHub-Actions"
    TeamName    = var.team_name
  }

  depends_on = [module.account_factory]
}

# Create staging environment in the new account
module "staging_environment" {
  source = "../../modules/environment"
  
  providers = {
    aws = aws.team_account_staging
  }

  team_name   = var.team_name
  environment = "staging"
  vpc_cidr    = var.staging_vpc_cidr

  common_tags = {
    Product     = "Hospital-Landing-Zone"
    Environment = "staging"
    Component   = "Landing-Zone"
    ManagedBy   = "Terraform"
    CreatedBy   = "GitHub-Actions"
    TeamName    = var.team_name
  }

  depends_on = [module.account_factory]
}

# Create prod environment in the new account
module "prod_environment" {
  source = "../../modules/environment"
  
  providers = {
    aws = aws.team_account_prod
  }

  team_name   = var.team_name
  environment = "prod"
  vpc_cidr    = var.prod_vpc_cidr

  common_tags = {
    Product     = "Hospital-Landing-Zone"
    Environment = "prod"
    Component   = "Landing-Zone"
    ManagedBy   = "Terraform"
    CreatedBy   = "GitHub-Actions"
    TeamName    = var.team_name
  }

  depends_on = [module.account_factory]
}

# Configure AWS providers for each environment
provider "aws" {
  alias  = "team_account_dev"
  region = var.aws_region

  assume_role {
    role_arn = module.account_factory.cross_account_role_arn
  }

  default_tags {
    tags = {
      Product     = "Hospital-Landing-Zone"
      Environment = "dev"
      Component   = "Landing-Zone"
      ManagedBy   = "Terraform"
      CreatedBy   = "GitHub-Actions"
    }
  }
}

provider "aws" {
  alias  = "team_account_staging"
  region = var.aws_region

  assume_role {
    role_arn = module.account_factory.cross_account_role_arn
  }

  default_tags {
    tags = {
      Product     = "Hospital-Landing-Zone"
      Environment = "staging"
      Component   = "Landing-Zone"
      ManagedBy   = "Terraform"
      CreatedBy   = "GitHub-Actions"
    }
  }
}

provider "aws" {
  alias  = "team_account_prod"
  region = var.aws_region

  assume_role {
    role_arn = module.account_factory.cross_account_role_arn
  }

  default_tags {
    tags = {
      Product     = "Hospital-Landing-Zone"
      Environment = "prod"
      Component   = "Landing-Zone"
      ManagedBy   = "Terraform"
      CreatedBy   = "GitHub-Actions"
    }
  }
}
