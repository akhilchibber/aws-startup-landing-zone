output "vpc_id" {
  description = "VPC ID"
  value       = aws_vpc.environment.id
}

output "vpc_cidr" {
  description = "VPC CIDR block"
  value       = aws_vpc.environment.cidr_block
}

output "public_subnet_ids" {
  description = "Public subnet IDs"
  value       = aws_subnet.public[*].id
}

output "private_subnet_ids" {
  description = "Private subnet IDs"
  value       = aws_subnet.private[*].id
}

output "nat_gateway_ids" {
  description = "NAT Gateway IDs"
  value       = aws_nat_gateway.environment[*].id
}

output "internet_gateway_id" {
  description = "Internet Gateway ID"
  value       = aws_internet_gateway.environment.id
}

output "flow_log_group_name" {
  description = "CloudWatch Log Group for VPC Flow Logs"
  value       = aws_cloudwatch_log_group.environment.name
}
