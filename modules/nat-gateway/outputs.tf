output "id" {
  description = "NAT Gateway ID"
  value       = aws_nat_gateway.main.id
}

output "public_ip" {
  description = "Public IP address of the NAT Gateway"
  value       = aws_nat_gateway.main.public_ip
}
