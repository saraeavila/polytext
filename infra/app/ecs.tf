resource "aws_ecs_cluster" "main" {
  name = "${local.name_prefix}-cluster"

  tags = local.common_tags
}

resource "aws_ecs_task_definition" "polytext" {
  family                   = "${local.name_prefix}-api"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"

  cpu    = tostring(var.ecs_cpu)
  memory = tostring(var.ecs_memory)

  execution_role_arn = aws_iam_role.ecs_execution.arn
  task_role_arn      = aws_iam_role.ecs_task.arn

  runtime_platform {
    operating_system_family = "LINUX"
    cpu_architecture        = "ARM64"
  }

  container_definitions = jsonencode([
    {
      name      = "polytext-api"
      image     = "${aws_ecr_repository.polytext.repository_url}:${var.image_tag}"
      essential = true

      portMappings = [
        {
          containerPort = 8000
          hostPort      = 8000
          protocol      = "tcp"
          appProtocol   = "http"
        }
      ]

      environment = [
        {
          name  = "ENVIRONMENT"
          value = var.environment
        },
        {
          name  = "LOG_LEVEL"
          value = "INFO"
        },
        {
          name  = "ALLOWED_HOSTS"
          value = "*"
        },
        {
          name  = "DATABASE_HOST"
          value = aws_db_instance.postgres.address
        },
        {
          name  = "DATABASE_PORT"
          value = tostring(aws_db_instance.postgres.port)
        },
        {
          name  = "DATABASE_NAME"
          value = "polytext"
        },
        {
          name  = "DATABASE_SSLMODE"
          value = "require"
        },
        {
          name  = "REDIS_URL"
          value = "rediss://${aws_elasticache_serverless_cache.valkey.endpoint[0].address}:${aws_elasticache_serverless_cache.valkey.endpoint[0].port}/0"
        }
      ]

      secrets = [
        {
          name      = "POLYTEXT_ADMIN_KEY"
          valueFrom = aws_secretsmanager_secret.polytext_admin_key.arn
        },
        {
          name      = "DATABASE_USER"
          valueFrom = "${aws_db_instance.postgres.master_user_secret[0].secret_arn}:username::"
        },
        {
          name      = "DATABASE_PASSWORD"
          valueFrom = "${aws_db_instance.postgres.master_user_secret[0].secret_arn}:password::"
        }
      ]

      logConfiguration = {
        logDriver = "awslogs"

        options = {
          awslogs-group         = aws_cloudwatch_log_group.polytext.name
          awslogs-region        = var.aws_region
          awslogs-stream-prefix = "polytext"
        }
      }

      healthCheck = {
        command = [
          "CMD-SHELL",
          "python -c \"import urllib.request; urllib.request.urlopen('http://localhost:8000/health')\" || exit 1"
        ]

        interval    = 30
        timeout     = 5
        retries     = 3
        startPeriod = 120
      }
    }
  ])

  tags = local.common_tags
}

resource "aws_ecs_service" "polytext" {
  name            = "${local.name_prefix}-service"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.polytext.arn
  desired_count   = var.ecs_desired_count
  launch_type     = "FARGATE"

  health_check_grace_period_seconds = 300

  deployment_circuit_breaker {
    enable   = true
    rollback = true
  }

  network_configuration {
    subnets = [
      aws_subnet.public_a.id,
      aws_subnet.public_b.id
    ]

    security_groups = [
      aws_security_group.ecs.id
    ]

    assign_public_ip = true
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.polytext.arn
    container_name   = "polytext-api"
    container_port   = 8000
  }

  depends_on = [
    aws_lb_listener.http
  ]

  tags = local.common_tags
}
