# --------------------------------
# ECS Assume Role Policy
# --------------------------------

data "aws_iam_policy_document" "ecs_tasks_assume_role" {
  statement {
    effect = "Allow"

    principals {
      type = "Service"

      identifiers = [
        "ecs-tasks.amazonaws.com"
      ]
    }

    actions = [
      "sts:AssumeRole"
    ]
  }
}


# --------------------------------
# ECS Task Execution Role
#
# Used by ECS/Fargate itself.
# --------------------------------

resource "aws_iam_role" "ecs_execution" {
  name = "${local.name_prefix}-ecs-execution-role"

  assume_role_policy = data.aws_iam_policy_document.ecs_tasks_assume_role.json

  tags = local.common_tags
}


resource "aws_iam_role_policy_attachment" "ecs_execution" {
  role       = aws_iam_role.ecs_execution.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}


# Allow ECS to retrieve the secrets that will be injected
# into the PolyText container.
data "aws_iam_policy_document" "ecs_execution_secrets" {
  statement {
    effect = "Allow"

    actions = [
      "secretsmanager:GetSecretValue"
    ]

    resources = [
      aws_secretsmanager_secret.polytext_admin_key.arn,
      aws_db_instance.postgres.master_user_secret[0].secret_arn
    ]
  }
}


resource "aws_iam_role_policy" "ecs_execution_secrets" {
  name = "${local.name_prefix}-ecs-secrets-policy"
  role = aws_iam_role.ecs_execution.id

  policy = data.aws_iam_policy_document.ecs_execution_secrets.json
}


# --------------------------------
# ECS Task Role
#
# Used by PolyText application code.
# --------------------------------

resource "aws_iam_role" "ecs_task" {
  name = "${local.name_prefix}-ecs-task-role"

  assume_role_policy = data.aws_iam_policy_document.ecs_tasks_assume_role.json

  tags = local.common_tags
}
