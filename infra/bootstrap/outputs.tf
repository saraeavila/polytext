output "terraform_state_bucket" {
  description = "S3 bucket used for Terraform remote state"
  value       = aws_s3_bucket.terraform_state.bucket
}

output "ecr_repository_url" {
  description = "PolyText API ECR repository URL"
  value       = aws_ecr_repository.polytext_api.repository_url
}
