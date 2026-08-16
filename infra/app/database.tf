resource "aws_db_subnet_group" "postgres" {
  name = "${local.name_prefix}-postgres-subnet-group"

  subnet_ids = [
    aws_subnet.private_a.id,
    aws_subnet.private_b.id
  ]

  tags = merge(local.common_tags, {
    Name = "${local.name_prefix}-postgres-subnet-group"
  })
}

resource "aws_db_instance" "postgres" {
  identifier = "${local.name_prefix}-postgres"

  engine         = "postgres"
  engine_version = "17"

  instance_class        = "db.t4g.micro"
  allocated_storage     = 20
  max_allocated_storage = 50
  storage_type          = "gp3"
  storage_encrypted     = true

  db_name  = "polytext"
  username = "polytext"

  manage_master_user_password = true

  db_subnet_group_name = aws_db_subnet_group.postgres.name

  vpc_security_group_ids = [
    aws_security_group.postgres.id
  ]

  publicly_accessible = false

  multi_az = false

  backup_retention_period = 1

  deletion_protection = false
  skip_final_snapshot = true

  auto_minor_version_upgrade = true

  tags = merge(local.common_tags, {
    Name = "${local.name_prefix}-postgres"
  })
}
