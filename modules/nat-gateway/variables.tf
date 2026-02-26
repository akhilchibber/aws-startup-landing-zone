variable "eip_allocation_id" {
  description = "Elastic IP allocation ID"
  type        = string
}

variable "public_subnet_id" {
  description = "Public Subnet ID"
  type        = string
}

variable "availability_zone" {
  description = "Availability zone"
  type        = string
}

variable "common_tags" {
  description = "Common tags to apply to all resources"
  type        = map(string)
}
