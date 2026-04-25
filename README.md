# hng14-stage2-devops

A containerized microservices job processing system built for the HNG Stage 2 DevOps task.

## Overview

This project contains four services:

- `frontend` - Node.js/Express UI for submitting and tracking jobs
- `api` - FastAPI service for creating jobs and returning job status
- `worker` - Python worker that processes queued jobs
- `redis` - queue and status store shared by the API and worker

Users submit jobs from the frontend. The frontend sends the request to the API. The API creates a job, stores its status in Redis, and pushes the job into a Redis queue. The worker consumes jobs from the queue and updates their status to `completed`.

## Architecture

- Frontend listens on port `3000`
- API listens on port `8000`
- Redis listens internally on port `6379`
- Worker communicates with Redis over the internal Docker network

## Prerequisites

Install the following before running the project:

- Git
- Docker Desktop
- Docker Compose
- Python 3.11 or later for local API testing
- Node.js 20 or later for local frontend linting

## Environment Setup

Create a root `.env` file from `.env.example`.

Example:

```env
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_PASSWORD=your_real_redis_password
QUEUE_NAME=job
PROCESSING_DELAY=2
APP_ENV=production
FRONTEND_PORT=3000
API_URL=http://api:8000
API_PORT=8000
```

Do not commit `.env`.

## Project Structure

```text
.
├── .github/workflows/ci-cd.yml
├── api
│   ├── Dockerfile
│   ├── main.py
│   ├── requirements.txt
│   ├── requirements-dev.txt
│   └── tests/test_main.py
├── frontend
│   ├── Dockerfile
│   ├── app.js
│   ├── package.json
│   ├── eslint.config.js
│   └── views/index.html
├── worker
│   ├── Dockerfile
│   ├── worker.py
│   └── requirements.txt
├── docker-compose.yml
├── .env.example
├── .gitignore
├── FIXES.md
└── README.md
```

## Running The Full Stack

From the repository root:

```bash
docker compose build
docker compose up
```

To run in the background:

```bash
docker compose up -d --build
```

## Confirming Successful Startup

A successful startup should show:

- Redis becomes healthy
- API becomes healthy
- Frontend starts successfully
- Worker stays running without crashing

You can verify with:

```bash
docker compose ps
curl http://localhost:8000/health
curl http://localhost:3000/health
```

Expected API health response:

```json
{"status":"ok"}
```

## Using The Application

1. Open the frontend in your browser:
   `http://localhost:3000`
2. Click `Submit New Job`
3. Watch the job status move from `queued` to `completed`

## Running Checks Locally

### API tests

```bash
PYTHONPATH=. pytest --cov=api --cov-report=xml api/tests
```

### Python lint

```bash
pip install -r api/requirements.txt
pip install -r api/requirements-dev.txt
flake8 api
```

### Frontend lint

```bash
cd frontend
npm install
npm run lint
```

## CI/CD Pipeline

GitHub Actions runs the pipeline in this order:

1. `lint`
2. `test`
3. `build`
4. `security-scan`
5. `integration-test`
6. `deploy`

### Stage Summary

- `lint`
  - runs `flake8` for Python
  - runs `eslint` for JavaScript
  - runs `hadolint` for Dockerfiles
- `test`
  - runs API unit tests with mocked Redis
  - generates and uploads a coverage report
- `build`
  - builds API, worker, and frontend images
  - tags images with both `latest` and the Git SHA
  - pushes images to a local registry service in the workflow
- `security-scan`
  - scans images with Trivy
  - fails on `CRITICAL` findings
  - uploads SARIF reports as artifacts
- `integration-test`
  - starts the full stack inside the runner
  - submits a job through the frontend
  - polls until the job completes
  - tears the stack down cleanly
- `deploy`
  - runs only on pushes to `main`
  - validates a candidate API container before replacement
  - re-checks final API and frontend health after replacement

## Notes

- Redis is not exposed to the host machine
- All service configuration comes from environment variables
- All application services run as non-root users inside their containers

## Documentation

- `README.md` explains setup and usage
- `FIXES.md` documents all identified issues and corrections
- `.env.example` lists all required configuration variables
