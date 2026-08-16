resource "aws_cloudwatch_log_group" "polytext" {
  name              = "/ecs/${local.name_prefix}"
  retention_in_days = 7

  tags = local.common_tags
}
