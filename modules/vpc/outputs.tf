output "id" {
  description = "VPC ID"
  value       = aws_vpc.main.id
}

output "cidr_block" {
  description = "VPC CIDR block"
  value       = aws_vpc.main.cidr_block
}
