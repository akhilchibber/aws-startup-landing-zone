# Environment Module - FREE TIER OPTIMIZED
# Creates environment structure optimized for AWS Free Tier ($0/month)
# 
# Changes from standard version:
# - Removed NAT Gateway (saves $45/month)
# - Removed Elastic IP (saves $3.50/month if unused)
# - Removed VPC Flow Logs (saves $1-5/month)
# - Removed private subnets (not needed without NAT)
# - Uses public subnets only
#
# Trade-offs:
# - All resources must be in public subnets
# - No network isolation between public/private
# - Suitable for: Development, testing, learning
# - NOT suitable for: Production, sensitive data

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# Create VPC for this environment
resource "aws_vpc" "environment" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = merge(
    var.common_tags,
    {
      Name        = "${var.team_name}-${var.environment}-vpc"
      Environment = var.environment
      Team        = var.team_name
      CostProfile = "FreeTier"
    }
  )
}

# Internet Gateway
resource "aws_internet_gateway" "environment" {
  vpc_id = aws_vpc.environment.id

  tags = merge(
    var.common_tags,
    {
      Name        = "${var.team_name}-${var.environment}-igw"
      Environment = var.environment
    }
  )
}

# Public Subnets (Multi-AZ for high availability)
resource "aws_subnet" "public" {
  count                   = 2
  vpc_id                  = aws_vpc.environment.id
  cidr_block              = cidrsubnet(var.vpc_cidr, 2, count.index)
  availability_zone       = data.aws_availability_zones.available.names[count.index]
  map_public_ip_on_launch = true

  tags = merge(
    var.common_tags,
    {
      Name        = "${var.team_name}-${var.environment}-public-subnet-${count.index + 1}"
      Environment = var.environment
      Type        = "Public"
    }
  )
}

# Public Route Table
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.environment.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.environment.id
  }

  tags = merge(
    var.common_tags,
    {
      Name        = "${var.team_name}-${var.environment}-public-rt"
      Environment = var.environment
    }
  )
}

# Associate public subnets with public route table
resource "aws_route_table_association" "public" {
  count          = 2
  subnet_id      = aws_subnet.public[count.index].id
  route_table_id = aws_route_table.public.id
}

# Data source for availability zones
data "aws_availability_zones" "available" {
  state = "available"
}
