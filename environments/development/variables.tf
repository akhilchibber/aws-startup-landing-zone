variable "aws_region" {
  description = "AWS region"
  type        = string
}

variable "aws_availability_zones" {
  description = "List of availability zones"
  type        = list(string)
}

variable "aws_elastic_ip_allocation_ids" {
  description = "List of Elastic IP allocation IDs for NAT Gateways"
  type        = list(string)
  sensitive   = true
}

variable "vpc_cidr" {
  description = "CIDR block for the VPC"
  type        = string
}

variable "public_subnet_cidrs" {
  description = "Map of public subnet CIDRs by availability zone"
  type        = map(string)
}

variable "private_subnet_cidrs" {
  description = "Map of private subnet CIDRs by availability zone"
  type        = map(string)
}

variable "enable_vpc_flow_logs" {
  description = "Enable VPC Flow Logs"
  type        = bool
  default     = true
}

variable "environment" {
  description = "Environment name (d=development, s=staging, p=production)"
  type        = string
  validation {
    condition     = contains(["d", "s", "p"], var.environment)
    error_message = "Environment must be 'd' (development), 's' (staging), or 'p' (production)."
  }
}

variable "product" {
  description = "Product name"
  type        = string
}
