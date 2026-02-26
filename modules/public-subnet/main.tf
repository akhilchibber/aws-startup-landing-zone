locals {
  subnet_component = "public-subnet"
  rt_component     = "public-rt"
}

resource "aws_subnet" "main" {
  vpc_id                  = var.vpc_id
  cidr_block              = var.cidr_block
  availability_zone       = var.availability_zone
  map_public_ip_on_launch = false

  tags = merge(
    var.common_tags,
    {
      Component = local.subnet_component
      Name      = join("-", [var.common_tags.Environment, var.common_tags.Product, local.subnet_component, var.availability_zone])
    }
  )
}

resource "aws_route_table" "main" {
  vpc_id = var.vpc_id

  tags = merge(
    var.common_tags,
    {
      Component = local.rt_component
      Name      = join("-", [var.common_tags.Environment, var.common_tags.Product, local.rt_component, var.availability_zone])
    }
  )
}

resource "aws_route" "internet_gateway" {
  route_table_id         = aws_route_table.main.id
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = var.internet_gateway_id
}

resource "aws_route_table_association" "main" {
  subnet_id      = aws_subnet.main.id
  route_table_id = aws_route_table.main.id
}
