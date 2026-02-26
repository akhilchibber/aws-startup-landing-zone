# Environment Module
# Creates dev/staging/prod environment structure within a team account

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
    }
  )
}

# Enable VPC Flow Logs
resource "aws_cloudwatch_log_group" "environment" {
  name              = "/aws/vpc/flowlogs/${var.team_name}-${var.environment}"
  retention_in_days = 7

  tags = var.common_tags
}

resource "aws_iam_role" "flowlog" {
  name = "${var.team_name}-${var.environment}-flowlog-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "vpc-flow-logs.amazonaws.com"
        }
        Action = "sts:AssumeRole"
      }
    ]
  })

  tags = var.common_tags
}

resource "aws_iam_role_policy" "flowlog" {
  name = "${var.team_name}-${var.environment}-flowlog-policy"
  role = aws_iam_role.flowlog.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents",
          "logs:DescribeLogGroups",
          "logs:DescribeLogStreams"
        ]
        Resource = "*"
      }
    ]
  })
}

resource "aws_flow_log" "environment" {
  iam_role_arn    = aws_iam_role.flowlog.arn
  log_destination = "${aws_cloudwatch_log_group.environment.arn}:*"
  traffic_type    = "ALL"
  vpc_id          = aws_vpc.environment.id

  tags = var.common_tags
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

# Public Subnets
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

# Private Subnets
resource "aws_subnet" "private" {
  count             = 2
  vpc_id            = aws_vpc.environment.id
  cidr_block        = cidrsubnet(var.vpc_cidr, 2, count.index + 2)
  availability_zone = data.aws_availability_zones.available.names[count.index]

  tags = merge(
    var.common_tags,
    {
      Name        = "${var.team_name}-${var.environment}-private-subnet-${count.index + 1}"
      Environment = var.environment
      Type        = "Private"
    }
  )
}

# Elastic IP for NAT Gateway (single NAT for cost optimization)
resource "aws_eip" "nat" {
  domain = "vpc"

  tags = merge(
    var.common_tags,
    {
      Name        = "${var.team_name}-${var.environment}-eip"
      Environment = var.environment
    }
  )

  depends_on = [aws_internet_gateway.environment]
}

# NAT Gateway (single NAT for cost optimization)
resource "aws_nat_gateway" "environment" {
  allocation_id = aws_eip.nat.id
  subnet_id     = aws_subnet.public[0].id

  tags = merge(
    var.common_tags,
    {
      Name        = "${var.team_name}-${var.environment}-nat"
      Environment = var.environment
    }
  )

  depends_on = [aws_internet_gateway.environment]
}

# Public Route Table
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.environment.id

  route {
    cidr_block      = "0.0.0.0/0"
    gateway_id      = aws_internet_gateway.environment.id
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

# Private Route Table (shared across AZs, single NAT for cost optimization)
resource "aws_route_table" "private" {
  vpc_id = aws_vpc.environment.id

  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.environment.id
  }

  tags = merge(
    var.common_tags,
    {
      Name        = "${var.team_name}-${var.environment}-private-rt"
      Environment = var.environment
    }
  )
}

# Associate private subnets with private route table
resource "aws_route_table_association" "private" {
  count          = 2
  subnet_id      = aws_subnet.private[count.index].id
  route_table_id = aws_route_table.private.id
}

# Data source for availability zones
data "aws_availability_zones" "available" {
  state = "available"
}
