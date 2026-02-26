locals {
  component = "nat-gateway"
}

resource "aws_nat_gateway" "main" {
  allocation_id = var.eip_allocation_id
  subnet_id     = var.public_subnet_id

  depends_on = []

  tags = merge(
    var.common_tags,
    {
      Component = local.component
      Name      = join("-", [var.common_tags.Environment, var.common_tags.Product, local.component, var.availability_zone])
    }
  )
}
