# PolyText AWS Deployment

PolyText includes Terraform infrastructure for deploying the API to AWS using:

- Amazon ECR
- Amazon ECS Fargate
- Application Load Balancer
- Amazon RDS for PostgreSQL
- Amazon ElastiCache Serverless for Valkey
- AWS Secrets Manager
- Amazon CloudWatch
- IAM
- VPC networking and security groups

## Architecture

Internet
→ Application Load Balancer
→ ECS Fargate
→ PolyText FastAPI container
→ RDS PostgreSQL
→ ElastiCache Valkey

The database and cache run in private subnets and are not directly accessible
from the public internet.

## Local Infrastructure Validation

Terraform configuration can be checked without deploying AWS resources:

```bash
make infra-check
```
