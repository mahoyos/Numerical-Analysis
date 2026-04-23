# Numerical Analysis Calculator

Comprehensive web platform to solve and visualize Numerical Analysis methods.

This repository is a monorepo with:
- Backend API in FastAPI (Python).
- Frontend SPA in Vue 3 + Vite + TypeScript.
- Infrastructure as Code in Terraform (AWS ECS Fargate + ALB).
- CI/CD in GitHub Actions with quality/security analysis and automated deployments.

## Team
- Juan Manuel Gomez Piedrahita
- Miguel Angel Hoyos
- Luisa Maria Alvarez Garcia
- Sebastian Restrepo Ortiz

## Table Of Contents
1. [What This Project Is](#what-this-project-is)
2. [Implemented Numerical Methods](#implemented-numerical-methods)
3. [High-Level Architecture](#high-level-architecture)
4. [Repository Structure](#repository-structure)
5. [Backend Design](#backend-design)
6. [Frontend Design](#frontend-design)
7. [Local Execution](#local-execution)
8. [Testing Strategy](#testing-strategy)
9. [Coverage And SonarCloud](#coverage-and-sonarcloud)
10. [CI/CD Pipelines](#cicd-pipelines)
11. [Infrastructure (Terraform + AWS)](#infrastructure-terraform--aws)
12. [Rollback Workflow](#rollback-workflow)
13. [Configuration And Secrets](#configuration-and-secrets)
14. [Operational Notes](#operational-notes)
15. [Current Pipeline Behavior](#current-pipeline-behavior)

## What This Project Is

The application allows users to input mathematical problems and solve them with classical numerical methods, while also visualizing iterative behavior and interpolation/system plots.

The goal is not only to compute results but to support learning and analysis through:
- Iteration tables.
- Error tracking.
- Method-specific inputs.
- Graphical visualization.

## Implemented Numerical Methods

### Non-linear equations
- Bisection
- False Position (Regula Falsi)
- Newton-Raphson
- Secant
- Fixed Point
- Multiple Roots

### Systems of equations
- Jacobi
- Gauss-Seidel
- SOR (Successive Over-Relaxation)

### Interpolation
- Newton interpolation
- Lagrange interpolation
- Spline interpolation
- Vandermonde interpolation

## High-Level Architecture

Runtime flow in cloud:

1. User accesses ALB on port `80`.
2. ALB routes frontend traffic to the frontend container (Nginx).
3. Frontend sends API calls to `/api/*`.
4. Nginx reverse-proxies `/api/*` to backend inside the same ECS task (`localhost:8000`).
5. FastAPI processes request, runs numerical method service, returns JSON response.

Key architectural decisions:
- Frontend and backend are packaged as separate images.
- Both run as containers in one ECS Fargate task definition.
- Infrastructure is fully reproducible with Terraform.
- CI/CD drives tests, quality checks, image build/push, and environment deployment.

## Repository Structure

```text
.
|-- backend/
|   |-- app.py
|   |-- models/
|   |-- routers/
|   |-- services/
|   |-- utils/
|   `-- tests/
|-- frontend/
|   |-- src/
|   |-- tests/
|   |-- cypress/
|   |-- nginx.conf
|   `-- vite.config.ts
|-- infra/
|   |-- main.tf
|   |-- variables.tf
|   `-- outputs.tf
|-- .github/workflows/
|   |-- ci-cd.yml
|   `-- rollback.yml
|-- docker-compose.yml
`-- sonar-project.properties
```

## Backend Design

Backend stack:
- FastAPI
- Pydantic models
- SymPy/Numpy/Math utilities for computations

Entry point:
- `backend/app.py`

Main features:
- CORS enabled.
- Health endpoint `GET /health` for load balancer checks.
- Three domain routers:
  - `backend/routers/non_linear_equations.py`
  - `backend/routers/system_equations.py`
  - `backend/routers/interpolation.py`

Domain layering:
- `models/`: input contracts.
- `routers/`: HTTP orchestration.
- `services/`: method execution/business logic.
- `utils/`: shared operations, error models and handlers.

## Frontend Design

Frontend stack:
- Vue 3 + TypeScript
- Vite
- Vue Router
- Axios
- Chart.js and chart plugins

Main behavior:
- SPA served by Nginx.
- API calls target `/api/`.
- Reverse proxy in `frontend/nginx.conf` forwards `/api/*` to backend on `localhost:8000`.

Important scripts (from `frontend/package.json`):
- `npm run dev`
- `npm run build`
- `npm run test:coverage`
- `npm run test:e2e`
- `npm run test:e2e:smoke`
- `npm run test:e2e:acceptance`

## Local Execution

### Option A: Docker Compose (recommended quick start)

From repository root:

```bash
docker compose up --build
```

Services:
- Frontend: `http://localhost`
- Backend: `http://localhost:8000`

### Option B: Run backend and frontend separately

Backend:

```bash
cd backend
pip install -r requirements.txt
python app.py
```

Frontend:

```bash
cd frontend
npm install
npm run dev
```

## Testing Strategy

The repository uses multiple test levels.

### Backend tests
- Framework: `pytest`
- Coverage configured in `backend/pytest.ini`
- Coverage fail-under currently set to `90`
- Markers available:
  - `smoke`
  - `acceptance`

Examples:

```bash
cd backend
pytest -q
pytest -q -m smoke --no-cov
pytest -q -m acceptance --no-cov
```

### Frontend unit tests
- Framework: `Vitest` + `@vue/test-utils`
- Coverage reporter: `text`, `html`, `lcov`
- Thresholds in `frontend/vite.config.ts`:
  - statements `90`
  - branches `90`
  - functions `90`
  - lines `90`

Example:

```bash
cd frontend
npm run test:coverage
```

### Frontend E2E tests
- Framework: `Cypress`
- Dedicated smoke and acceptance scripts included.

Examples:

```bash
cd frontend
npm run test:e2e:smoke
npm run test:e2e:acceptance
```

## Coverage And SonarCloud

Sonar configuration is in `sonar-project.properties`.

Current highlights:
- Project key and organization configured.
- Backend coverage imported from `coverage.xml`.
- Frontend coverage imported from `frontend/coverage/lcov.info`.
- `sonar.qualitygate.wait=true` with timeout.
- Test paths and coverage exclusions are explicitly configured.

If Sonar analysis fails, verify:
- `SONAR_TOKEN` secret permissions.
- Correct `sonar.projectKey` and `sonar.organization`.
- `SONAR_HOST_URL` value for SonarCloud (`https://sonarcloud.io`).

## CI/CD Pipelines

Main pipeline file: `.github/workflows/ci-cd.yml`

### Trigger strategy
- `push` to `main` and `release`
- `pull_request` to `main` and `release`
- `workflow_dispatch`

### Pipeline stages

1. Path filtering
- Detects backend/frontend/infra changes.
- Skips irrelevant jobs for monorepo efficiency.

2. Backend quality and tests
- Installs Python dependencies.
- Runs formatter/linter/tests.
- Publishes `coverage.xml`, `pylint-report.txt`, `flake8-report.txt` as artifacts.

3. Frontend quality and tests
- Installs Node dependencies.
- Runs ESLint and Vitest coverage.
- Publishes `frontend/coverage` artifacts.

4. SonarCloud scan
- Downloads backend/frontend artifacts.
- Executes Sonar scanner action.

5. IaC scan
- Runs Checkov against `infra/`.

6. Build and push images
- Builds backend and frontend Docker images.
- Pushes tags `latest` and `${GITHUB_SHA}` to DockerHub.
- Runs Trivy scan on both images.

7. Staging deployment (release branch)
- Terraform init/apply with staging state key.
- Captures previous backend/frontend image URIs from Terraform state before deploy.
- Updates ECS staging service.

8. Production deployment (main branch)
- Terraform init/apply with production state key.
- Captures previous backend/frontend image URIs from Terraform state before deploy.
- Updates ECS production service.

9. Post-deploy smoke checks (automatic)
- Runs after staging deploy (`release`) and production deploy (`main`).
- Validates frontend availability on ALB URL.
- Validates backend health through frontend reverse proxy at `/api/health`.

10. Auto rollback on smoke failure (automatic)
- If smoke fails in staging or production, pipeline runs rollback automatically.
- Rollback re-applies Terraform with the previous backend/frontend image URIs captured before deployment.
- Waits for ECS service stability after rollback.

## Infrastructure (Terraform + AWS)

Terraform files live in `infra/`.

### Provisioned resources
- ECS Cluster
- ECS Task Definition (2 containers: backend + frontend)
- ECS Service (Fargate)
- Application Load Balancer (ALB)
- Target Group backend (port 8000, health `/health`)
- Target Group frontend (port 80, health `/`)
- Listeners for port 80 and 8000
- Security Groups for ALB and ECS service
- CloudWatch Log Group

### State backend
- Remote state in S3 bucket (created/validated in pipeline).

### Core Terraform variables
- `environment_name` (`staging` or `production`)
- `backend_image_uri`
- `frontend_image_uri`
- `lab_role_arn`
- `vpc_id`
- `subnet_ids`
- `aws_region` (default `us-east-1`)

### Useful outputs
- `alb_dns_name`
- `alb_url`
- `ecs_cluster_name`
- `ecs_service_name`

## Rollback Workflow

Rollback is available in two modes:

1. Automatic rollback inside main CI/CD pipeline (`.github/workflows/ci-cd.yml`)
2. Manual panic-button rollback (`.github/workflows/rollback.yml`)

### Automatic rollback (in ci-cd)

Characteristics:
- Triggered only when post-deploy smoke tests fail.
- Implemented for both `release` (staging) and `main` (production).
- Uses previous image URIs captured from Terraform state before deployment.
- Applies Terraform with previous images and waits for ECS service stability.
- Requires that a previous deploy exists (first deploy has no previous image to restore).

### Manual rollback (panic button)

Characteristics:
- Manual trigger (`workflow_dispatch`).
- Accepts optional backend/frontend image tags.
- Requires at least one tag to proceed.
- Applies Terraform on production with selected image URIs.
- Waits for ECS primary deployment to reach desired running tasks.

This acts as a manual safety net when you want to force a specific rollback target.

## Configuration And Secrets

### GitHub Secrets (expected)
- `SONAR_TOKEN`
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_SESSION_TOKEN`
- `DOCKERHUB_TOKEN`

### GitHub Variables (expected)
- `SONAR_HOST_URL`
- `DOCKERHUB_USERNAME`
- `TF_STATE_BUCKET`
- `LAB_ROLE_ARN`
- `VPC_ID`
- `SUBNET_IDS`
