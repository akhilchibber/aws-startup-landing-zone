variable "cidr" {
  description = "CIDR block for the VPC"
  type        = string
}

variable "flow_logs" {
  description = "Enable VPC Flow Logs"
  type        = bool
  default     = true
}

variable "common_tags" {
  description = "Common tags to apply to all resources"
  type        = map(string)
}
