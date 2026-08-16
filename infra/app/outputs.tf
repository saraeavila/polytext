output "vpc_id" {
  description = "ID of the PolyText VPC"
  value       = aws_vpc.main.id
}

output "public_subnet_ids" {
  description = "Public subnet IDs used by the ALB and ECS"
  value = [
    aws_subnet.public_a.id,
    aws_subnet.public_b.id
  ]
}

output "private_subnet_ids" {
  description = "Private subnet IDs used by data services"
  value = [
    aws_subnet.private_a.id,
    aws_subnet.private_b.id
  ]
}

output "alb_security_group_id" {
  description = "Security group used by the Application Load Balancer"
  value       = aws_security_group.alb.id
}

output "ecs_security_group_id" {
  description = "Security group used by ECS tasks"
  value       = aws_security_group.ecs.id
}

output "postgres_security_group_id" {
  description = "Security group used by PostgreSQL"
  value       = aws_security_group.postgres.id
}

output "valkey_security_group_id" {
  description = "Security group used by Valkey"
  value       = aws_security_group.valkey.id
}

output "postgres_endpoint" {
  description = "PostgreSQL RDS endpoint"
  value       = aws_db_instance.postgres.address
}

output "postgres_port" {
  description = "PostgreSQL RDS port"
  value       = aws_db_instance.postgres.port
}

output "valkey_endpoint" {
  description = "Valkey serverless endpoint"
  value       = aws_elasticache_serverless_cache.valkey.endpoint[0].address
}

output "valkey_port" {
  description = "Valkey serverless primary port"
  value       = aws_elasticache_serverless_cache.valkey.endpoint[0].port
}

output "ecs_execution_role_arn" {
  description = "IAM role used by ECS to launch PolyText tasks"
  value       = aws_iam_role.ecs_execution.arn
}

output "ecs_task_role_arn" {
  description = "IAM role assumed by the PolyText application"
  value       = aws_iam_role.ecs_task.arn
}

output "polytext_admin_secret_arn" {
  description = "Secrets Manager ARN for the PolyText admin key"
  value       = aws_secretsmanager_secret.polytext_admin_key.arn
}

output "postgres_master_secret_arn" {
  description = "RDS-managed PostgreSQL master credential secret ARN"
  value       = aws_db_instance.postgres.master_user_secret[0].secret_arn
}

output "ecs_cluster_name" {
  description = "PolyText ECS cluster name"
  value       = aws_ecs_cluster.main.name
}

output "ecs_task_definition_arn" {
  description = "PolyText ECS task definition ARN"
  value       = aws_ecs_task_definition.polytext.arn
}

output "cloudwatch_log_group_name" {
  description = "CloudWatch log group used by PolyText"
  value       = aws_cloudwatch_log_group.polytext.name
}

output "alb_dns_name" {
  description = "Public DNS name of the PolyText Application Load Balancer"
  value       = aws_lb.polytext.dns_name
}

output "ecs_service_name" {
  description = "PolyText ECS service name"
  value       = aws_ecs_service.polytext.name
}

output "polytext_api_url" {
  description = "HTTP URL for the deployed PolyText API"
  value       = "http://${aws_lb.polytext.dns_name}"
}

output "ecr_repository_url" {
  description = "ECR repository URL for the PolyText API image"
  value       = aws_ecr_repository.polytext.repository_url
}

output "deployed_image" {
  description = "Container image used by the PolyText ECS task"
  value       = "${aws_ecr_repository.polytext.repository_url}:${var.image_tag}"
}
