locals {
  vpc_component       = "vpc"
  flow_logs_component = "vpc-flow-logs"
  s3_bucket_component = "s3"
}

resource "aws_vpc" "main" {
  cidr_block           = var.cidr
  instance_tenancy     = "default"
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = merge(
    var.common_tags,
    {
      Component = local.vpc_component
      Name      = join("-", [var.common_tags.Environment, var.common_tags.Product, local.vpc_component])
    }
  )
}

resource "aws_flow_log" "main" {
  count = var.flow_logs ? 1 : 0

  log_destination      = aws_s3_bucket.vpc_flow_logs[0].arn
  log_destination_type = "s3"
  traffic_type         = "ALL"
  vpc_id               = aws_vpc.main.id

  tags = merge(
    var.common_tags,
    {
      Component = local.flow_logs_component
      Name      = join("-", [var.common_tags.Environment, var.common_tags.Product, local.flow_logs_component])
    }
  )
}

resource "aws_s3_bucket" "vpc_flow_logs" {
  count  = var.flow_logs ? 1 : 0
  bucket = "vpc-flow-logs-${aws_vpc.main.id}"

  tags = merge(
    var.common_tags,
    {
      Component = local.s3_bucket_component
      Name      = join("-", [var.common_tags.Environment, var.common_tags.Product, local.s3_bucket_component])
    }
  )
}

resource "aws_s3_bucket_versioning" "vpc_flow_logs" {
  count  = var.flow_logs ? 1 : 0
  bucket = aws_s3_bucket.vpc_flow_logs[0].id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "vpc_flow_logs" {
  count  = var.flow_logs ? 1 : 0
  bucket = aws_s3_bucket.vpc_flow_logs[0].id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_public_access_block" "vpc_flow_logs" {
  count  = var.flow_logs ? 1 : 0
  bucket = aws_s3_bucket.vpc_flow_logs[0].id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}
