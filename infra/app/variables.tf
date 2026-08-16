variable "aws_region" {
  description = "AWS region for PolyText"
  type        = string
  default     = "us-east-2"
}

variable "project_name" {
  description = "Name used to prefix PolyText AWS resources"
  type        = string
  default     = "polytext"
}

variable "environment" {
  description = "Deployment environment"
  type        = string
  default     = "production"

  validation {
    condition     = contains(["development", "staging", "production"], var.environment)
    error_message = "Environment must be development, staging, or production."
  }
}

variable "image_tag" {
  description = "Docker image tag deployed to ECS"
  type        = string
  default     = "latest"
}

variable "ecs_cpu" {
  description = "CPU units allocated to the PolyText Fargate task"
  type        = number
  default     = 1024
}

variable "ecs_memory" {
  description = "Memory in MiB allocated to the PolyText Fargate task"
  type        = number
  default     = 8192
}

variable "ecs_desired_count" {
  description = "Number of PolyText ECS tasks to run"
  type        = number
  default     = 1
}
