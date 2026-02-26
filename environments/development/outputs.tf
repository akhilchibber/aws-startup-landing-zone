output "vpc_id" {
  description = "VPC ID"
  value       = module.vpc.id
}

output "vpc_cidr" {
  description = "VPC CIDR block"
  value       = module.vpc.cidr_block
}

output "internet_gateway_id" {
  description = "Internet Gateway ID"
  value       = module.igw.id
}

output "public_subnets" {
  description = "Public Subnet IDs and details"
  value = {
    for az, subnet in module.public_subnet : az => {
      id               = subnet.id
      cidr_block       = subnet.cidr_block
      availability_zone = subnet.availability_zone
    }
  }
}

output "private_subnets" {
  description = "Private Subnet IDs and details"
  value = {
    for az, subnet in module.private_subnet : az => {
      id               = subnet.id
      cidr_block       = subnet.cidr_block
      availability_zone = subnet.availability_zone
    }
  }
}

output "nat_gateways" {
  description = "NAT Gateway IDs and public IPs"
  value = {
    for az, nat in module.nat_gateway : az => {
      id        = nat.id
      public_ip = nat.public_ip
    }
  }
}
