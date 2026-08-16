resource "aws_elasticache_serverless_cache" "valkey" {
  name   = "${local.name_prefix}-valkey"
  engine = "valkey"

  description = "Serverless Valkey cache for PolyText rate limiting"

  subnet_ids = [
    aws_subnet.private_a.id,
    aws_subnet.private_b.id
  ]

  security_group_ids = [
    aws_security_group.valkey.id
  ]

  tags = merge(local.common_tags, {
    Name = "${local.name_prefix}-valkey"
  })
}
