# PolyText

**PolyText** is a multilingual NLP API and interactive playground built to explore how machine-learning models can be exposed through a reliable, production-oriented software architecture.

The platform supports sentiment analysis, named-entity recognition, automatic language identification, and zero-shot classification. Rather than coupling API endpoints directly to individual models, PolyText uses language-aware model routing, multilingual fallbacks, lazy model loading, authentication, rate limiting, persistence, observability, and containerized infrastructure to treat NLP inference as a complete software system.

## Demo

> Interactive Playground screenshots coming soon.

The PolyText Playground provides a React-based interface for testing each NLP task, selecting or automatically detecting languages, inspecting model predictions, and viewing request latency.

## Features

### NLP

- Multilingual sentiment analysis
- Named-entity recognition
- Zero-shot text classification
- Automatic language detection with fastText
- Language-specific model routing
- Multilingual model fallbacks
- Lazy model loading and adapter caching
- Thread-safe model initialization

### API & Application

- FastAPI REST API
- Typed request and response contracts with Pydantic
- API-key authentication
- API-key creation, listing, and revocation
- Per-key Redis rate limiting
- PostgreSQL persistence
- Request usage tracking and analytics
- Health and dependency-readiness endpoints
- Production-aware API configuration

### Frontend

- React + TypeScript playground
- Sentiment, entity, and classification interfaces
- Automatic language detection
- Named-entity highlighting using character offsets
- Candidate-label input for zero-shot classification
- Request latency display
- API availability indicator
- Loading and error states
- Request cancellation and stale-response protection
- Responsive and keyboard-accessible interface
- Example prompts for each NLP task

### Infrastructure & Reliability

- Docker and Docker Compose
- Nginx frontend serving and API proxying
- PostgreSQL and Redis container services
- Prometheus metrics
- Structured request logging
- Unit and integration testing
- Frontend component and application testing
- Locust load testing
- GitHub Actions CI
- Deployment-ready Terraform for AWS

---

## Architecture

PolyText separates the web interface, API layer, model routing, inference adapters, persistence, and infrastructure concerns rather than exposing machine-learning pipelines directly through HTTP endpoints.

See the full [architecture documentation](docs/architecture.md).

### Local Architecture

```text
Browser
   |
   v
React + TypeScript
   |
   v
Nginx
   |
   | /api
   v
FastAPI
   |
   +-------------------------+
   |                         |
   v                         v
PostgreSQL                 Redis
   |
   v
Usage / API-key data

FastAPI
   |
   v
Language Detection
   |
   v
Model Registry
   |
   +-------------------------------+
   |               |               |
   v               v               v
Sentiment          NER       Classification
Models             Model         Model
```

The entire local stack can be launched using Docker Compose.

---

## Model Routing

PolyText uses a model registry to separate API behavior from individual machine-learning implementations.

Model resolution follows:

```text
(task, language)
       |
       v
Exact language-specific model?
       |
    +--+--+
    |     |
   yes    no
    |     |
    v     v
specialist     multilingual fallback
                    |
                    v
             unsupported model
             if no fallback exists
```

For example:

```text
Sentiment + Spanish
        |
        v
Robertuito Spanish specialist
```

while:

```text
Sentiment + English
        |
        v
Multilingual XLM-RoBERTa fallback
```

This allows specialized language models to coexist with broader multilingual coverage without changing the API contract.

---

## NLP Models

| Task | Model | Role |
|---|---|---|
| Language Detection | fastText `lid.176` | Automatic language identification |
| Sentiment Analysis | `cardiffnlp/twitter-xlm-roberta-base-sentiment` | Multilingual fallback |
| Sentiment Analysis | `pysentimiento/robertuito-sentiment-analysis` | Spanish specialist |
| Named-Entity Recognition | `Davlan/xlm-roberta-base-ner-hrl` | Multilingual NER |
| Zero-Shot Classification | `MoritzLaurer/mDeBERTa-v3-base-mnli-xnli` | Multilingual zero-shot classification |

---

## Tech Stack

### Backend

- Python
- FastAPI
- Pydantic
- SQLAlchemy
- Alembic
- Uvicorn

### Machine Learning / NLP

- PyTorch
- Hugging Face Transformers
- fastText

### Data

- PostgreSQL
- Redis / Valkey

### Frontend

- React
- TypeScript
- Vite
- Nginx

### Infrastructure

- Docker
- Docker Compose
- Terraform
- AWS ECS / Fargate
- Amazon RDS
- Amazon ElastiCache
- Amazon ECR
- Application Load Balancer
- AWS Secrets Manager
- Amazon CloudWatch

### Testing & Observability

- pytest
- Vitest
- React Testing Library
- Locust
- Prometheus
- GitHub Actions

---

## Quick Start

### Prerequisites

You will need:

- Docker
- Docker Compose

### Start PolyText

From the repository root:

```bash
docker compose up -d --build
```

Once the containers are healthy, open:

```text
http://localhost:3000
```

The frontend is served through Nginx, which proxies API requests to the FastAPI service.

### Check Service Status

```bash
docker compose ps
```

Check the API directly:

```bash
curl http://localhost:8000/health
```

Or through the frontend proxy:

```bash
curl http://localhost:3000/api/health
```

### Stop PolyText

```bash
docker compose down
```

---

## API

Authenticated endpoints require a PolyText API key:

```http
Authorization: Bearer poly_sk_...
```

### Sentiment Analysis

```http
POST /v1/sentiment
```

Example request:

```json
{
  "text": "Me encanta este producto."
}
```

Example response:

```json
{
  "language": {
    "code": "es",
    "confidence": 0.99
  },
  "sentiment": {
    "label": "positive",
    "confidence": 0.98
  }
}
```

An optional `language` field can be supplied to bypass automatic language detection.

### Named-Entity Recognition

```http
POST /v1/entities
```

Example request:

```json
{
  "text": "Sara trabaja en Microsoft en Madrid."
}
```

Entity predictions include:

- entity text
- entity type
- character start offset
- character end offset
- confidence

Supported normalized labels include:

```text
person
organization
location
miscellaneous
```

### Zero-Shot Classification

```http
POST /v1/classify
```

Example request:

```json
{
  "text": "Apple announced a new artificial intelligence platform.",
  "candidate_labels": [
    "technology",
    "business",
    "sports",
    "politics"
  ]
}
```

Between 2 and 20 candidate labels can be supplied.

---

## Operational Endpoints

### Liveness

```http
GET /health
```

Reports whether the API process is running.

### Readiness

```http
GET /ready
```

Checks whether required dependencies, including PostgreSQL and Redis, are available.

### Metrics

```http
GET /metrics
```

Exposes Prometheus metrics.

In production configuration, operational endpoints and API documentation are hardened appropriately, including protection for metrics and disabling public Swagger/OpenAPI documentation.

---

## Authentication & Rate Limiting

PolyText issues API keys using the prefix:

```text
poly_sk_
```

API keys can be:

- created
- listed
- revoked

Inference requests are authenticated using Bearer tokens.

Redis provides atomic, per-key request counters for rate limiting. Each API key maintains an independent request allowance.

Administrative API-key provisioning is protected separately from normal inference authentication.

---

## Testing

### Backend Tests

From the repository root:

```bash
python -m pytest -q
```

The backend test suite covers API behavior, schemas, services, model adapters, registry behavior, authentication, rate limiting, configuration, and production hardening.

### Frontend Tests

```bash
cd frontend

npm test
npm run lint
npm run build
```

Frontend tests use Vitest and React Testing Library to cover individual components and full Playground workflows.

### Terraform Validation

```bash
make infra-check
```

This performs local Terraform initialization, formatting validation, and configuration validation without deploying AWS infrastructure.

---

## Load Testing

PolyText was load-tested with Locust after model and infrastructure integration.

A final 5-user run produced:

| Metric | Result |
|---|---:|
| Requests | 623 |
| Failures | 0 |
| Throughput | 3.47 requests/sec |
| Average latency | 438 ms |
| Median latency | 210 ms |

Classification is the most computationally expensive endpoint, while sentiment and NER maintain lower typical latency.

Load testing also exposed a concurrency issue in lazy Hugging Face model initialization. PolyText's shared model loader was subsequently redesigned using thread-safe, double-checked locking.

After the fix, concurrent load tests completed with **zero request failures**.

---

## Observability

PolyText exposes Prometheus metrics for:

- HTTP request counts
- HTTP request latency
- model resolutions
- model inference requests
- model inference duration
- rate-limit rejections

Structured application logs also record model-routing decisions, including whether a specialist or fallback model was selected.

---

## AWS Deployment Design

PolyText includes deployment-ready Terraform for an AWS architecture consisting of:

```text
Internet
   |
   v
Application Load Balancer
   |
   v
ECS Fargate
   |
   v
PolyText API
   |
   +------------------+
   |                  |
   v                  v
RDS PostgreSQL   ElastiCache Valkey
```

Supporting infrastructure includes:

- VPC networking
- public and private subnets
- security groups
- Amazon ECR
- ECS Fargate
- Application Load Balancer
- Amazon RDS
- ElastiCache Serverless for Valkey
- IAM roles
- AWS Secrets Manager
- Amazon CloudWatch

The AWS infrastructure is maintained as **deployment-ready infrastructure-as-code and is not provisioned by default**.

AWS operations are deliberately protected by an explicit Makefile safety gate.

For example:

```bash
make aws-plan
```

is blocked unless deployment is intentionally enabled.

See [AWS deployment documentation](docs/aws-deployment.md) for additional details.

---

## Project Structure

```text
polytext/
├── app/
│   ├── api/
│   ├── core/
│   ├── db/
│   ├── models/
│   └── services/
│
├── frontend/
│   ├── src/
│   │   ├── api/
│   │   ├── components/
│   │   ├── data/
│   │   └── types/
│   ├── Dockerfile
│   └── nginx.conf
│
├── tests/
├── load_tests/
├── infra/
│   ├── bootstrap/
│   └── app/
├── docs/
│   ├── architecture.md
│   └── aws-deployment.md
│
├── .github/
│   └── workflows/
├── Dockerfile
├── compose.yml
├── Makefile
└── README.md
```

---

## Design Goals

PolyText was designed around several engineering goals:

1. **Keep model-specific behavior behind adapters.**
2. **Separate API contracts from machine-learning implementations.**
3. **Route requests by language specificity with multilingual fallback.**
4. **Load expensive models only when they are needed.**
5. **Keep local development, testing, and deployment reproducible.**
6. **Treat authentication, persistence, rate limiting, observability, and failure handling as first-class parts of an ML system.**

The result is intended to demonstrate not only NLP inference, but the engineering required to expose machine-learning models as a maintainable software service.
