output "id" {
  description = "Private Subnet ID"
  value       = aws_subnet.main.id
}

output "cidr_block" {
  description = "Private Subnet CIDR block"
  value       = aws_subnet.main.cidr_block
}

output "availability_zone" {
  description = "Availability zone"
  value       = aws_subnet.main.availability_zone
}
