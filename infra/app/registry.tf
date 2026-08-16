resource "aws_ecr_repository" "polytext" {
  name                 = "${var.project_name}-api"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }

  tags = local.common_tags
}

resource "aws_ecr_lifecycle_policy" "polytext" {
  repository = aws_ecr_repository.polytext.name

  policy = jsonencode({
    rules = [
      {
        rulePriority = 1
        description  = "Keep only the five most recent images"

        selection = {
          tagStatus   = "any"
          countType   = "imageCountMoreThan"
          countNumber = 5
        }

        action = {
          type = "expire"
        }
      }
    ]
  })
}
