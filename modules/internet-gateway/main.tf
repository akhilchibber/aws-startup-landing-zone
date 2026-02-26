locals {
  component = "igw"
}

resource "aws_internet_gateway" "main" {
  vpc_id = var.vpc_id

  tags = merge(
    var.common_tags,
    {
      Component = local.component
      Name      = join("-", [var.common_tags.Environment, var.common_tags.Product, local.component])
    }
  )
}
