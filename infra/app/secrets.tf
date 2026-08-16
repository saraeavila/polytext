resource "aws_secretsmanager_secret" "polytext_admin_key" {
  name        = "${local.name_prefix}/admin-key"
  description = "PolyText administrative API key"

  # Appropriate for our temporary/demo deployment:
  # deleting the Terraform stack can remove this secret immediately.
  recovery_window_in_days = 0

  tags = merge(local.common_tags, {
    Name = "${local.name_prefix}-admin-key"
  })
}
