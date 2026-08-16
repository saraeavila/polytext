# -------------------------
# Application Load Balancer
# -------------------------

resource "aws_security_group" "alb" {
  name        = "${local.name_prefix}-alb-sg"
  description = "Security group for the PolyText Application Load Balancer"
  vpc_id      = aws_vpc.main.id

  tags = merge(local.common_tags, {
    Name = "${local.name_prefix}-alb-sg"
  })
}

resource "aws_vpc_security_group_ingress_rule" "alb_http" {
  security_group_id = aws_security_group.alb.id

  description = "Allow HTTP traffic from the internet"
  cidr_ipv4   = "0.0.0.0/0"
  from_port   = 80
  to_port     = 80
  ip_protocol = "tcp"
}

resource "aws_vpc_security_group_ingress_rule" "alb_https" {
  security_group_id = aws_security_group.alb.id

  description = "Allow HTTPS traffic from the internet"
  cidr_ipv4   = "0.0.0.0/0"
  from_port   = 443
  to_port     = 443
  ip_protocol = "tcp"
}

# -------------------------
# ECS / FastAPI
# -------------------------

resource "aws_security_group" "ecs" {
  name        = "${local.name_prefix}-ecs-sg"
  description = "Security group for PolyText ECS tasks"
  vpc_id      = aws_vpc.main.id

  tags = merge(local.common_tags, {
    Name = "${local.name_prefix}-ecs-sg"
  })
}

resource "aws_vpc_security_group_ingress_rule" "ecs_from_alb" {
  security_group_id = aws_security_group.ecs.id

  description                  = "Allow PolyText API traffic from the ALB"
  referenced_security_group_id = aws_security_group.alb.id
  from_port                    = 8000
  to_port                      = 8000
  ip_protocol                  = "tcp"
}

resource "aws_vpc_security_group_egress_rule" "alb_to_ecs" {
  security_group_id = aws_security_group.alb.id

  description                  = "Allow ALB traffic to PolyText ECS tasks"
  referenced_security_group_id = aws_security_group.ecs.id
  from_port                    = 8000
  to_port                      = 8000
  ip_protocol                  = "tcp"
}

# ECS needs HTTPS outbound access for services such as ECR,
# CloudWatch, and model downloads.
resource "aws_vpc_security_group_egress_rule" "ecs_https" {
  security_group_id = aws_security_group.ecs.id

  description = "Allow HTTPS outbound traffic"
  cidr_ipv4   = "0.0.0.0/0"
  from_port   = 443
  to_port     = 443
  ip_protocol = "tcp"
}

# -------------------------
# PostgreSQL / RDS
# -------------------------

resource "aws_security_group" "postgres" {
  name        = "${local.name_prefix}-postgres-sg"
  description = "Security group for PolyText PostgreSQL"
  vpc_id      = aws_vpc.main.id

  tags = merge(local.common_tags, {
    Name = "${local.name_prefix}-postgres-sg"
  })
}

resource "aws_vpc_security_group_ingress_rule" "postgres_from_ecs" {
  security_group_id = aws_security_group.postgres.id

  description                  = "Allow PostgreSQL traffic from PolyText ECS tasks"
  referenced_security_group_id = aws_security_group.ecs.id
  from_port                    = 5432
  to_port                      = 5432
  ip_protocol                  = "tcp"
}

resource "aws_vpc_security_group_egress_rule" "ecs_to_postgres" {
  security_group_id = aws_security_group.ecs.id

  description                  = "Allow ECS tasks to connect to PostgreSQL"
  referenced_security_group_id = aws_security_group.postgres.id
  from_port                    = 5432
  to_port                      = 5432
  ip_protocol                  = "tcp"
}

# -------------------------
# Valkey / ElastiCache
# -------------------------

resource "aws_security_group" "valkey" {
  name        = "${local.name_prefix}-valkey-sg"
  description = "Security group for PolyText Valkey"
  vpc_id      = aws_vpc.main.id

  tags = merge(local.common_tags, {
    Name = "${local.name_prefix}-valkey-sg"
  })
}

resource "aws_vpc_security_group_ingress_rule" "valkey_6379_from_ecs" {
  security_group_id = aws_security_group.valkey.id

  description                  = "Allow Valkey traffic from PolyText ECS tasks"
  referenced_security_group_id = aws_security_group.ecs.id
  from_port                    = 6379
  to_port                      = 6379
  ip_protocol                  = "tcp"
}

resource "aws_vpc_security_group_ingress_rule" "valkey_6380_from_ecs" {
  security_group_id = aws_security_group.valkey.id

  description                  = "Allow Valkey serverless traffic from PolyText ECS tasks"
  referenced_security_group_id = aws_security_group.ecs.id
  from_port                    = 6380
  to_port                      = 6380
  ip_protocol                  = "tcp"
}

resource "aws_vpc_security_group_egress_rule" "ecs_to_valkey_6379" {
  security_group_id = aws_security_group.ecs.id

  description                  = "Allow ECS tasks to connect to Valkey"
  referenced_security_group_id = aws_security_group.valkey.id
  from_port                    = 6379
  to_port                      = 6379
  ip_protocol                  = "tcp"
}

resource "aws_vpc_security_group_egress_rule" "ecs_to_valkey_6380" {
  security_group_id = aws_security_group.ecs.id

  description                  = "Allow ECS tasks to connect to Valkey serverless"
  referenced_security_group_id = aws_security_group.valkey.id
  from_port                    = 6380
  to_port                      = 6380
  ip_protocol                  = "tcp"
}
