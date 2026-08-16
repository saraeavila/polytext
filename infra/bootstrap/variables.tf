variable "aws_region" {
  description = "AWS region for PolyText infrastructure"
  type        = string
  default     = "us-east-2"
}

variable "project_name" {
  description = "Project name used for AWS resource naming"
  type        = string
  default     = "polytext"
}
