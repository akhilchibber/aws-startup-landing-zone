variable "vpc_id" {
  description = "VPC ID"
  type        = string
}

variable "cidr_block" {
  description = "CIDR block for the subnet"
  type        = string
}

variable "availability_zone" {
  description = "Availability zone for the subnet"
  type        = string
}

variable "nat_gateway_id" {
  description = "NAT Gateway ID"
  type        = string
}

variable "common_tags" {
  description = "Common tags to apply to all resources"
  type        = map(string)
}
