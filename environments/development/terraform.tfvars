aws_region                    = "eu-north-1"
aws_availability_zones        = ["eu-north-1a", "eu-north-1b"]
aws_elastic_ip_allocation_ids = ["eipalloc-06faaa96c6c589469", "eipalloc-06ad19500e7e33452"]
vpc_cidr                      = "10.0.0.0/16"
enable_vpc_flow_logs          = true
environment                   = "d"
product                       = "startup"

public_subnet_cidrs = {
  "eu-north-1a" = "10.0.0.0/24"
  "eu-north-1b" = "10.0.1.0/24"
}

private_subnet_cidrs = {
  "eu-north-1a" = "10.0.32.0/19"
  "eu-north-1b" = "10.0.64.0/19"
}
