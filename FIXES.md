# FIXES

This file documents the issues found in the starter repository and the changes made to fix them.

## 1. Tracked environment file committed to repository

- File: `api/.env`
- Line: 1-2
- Problem: A `.env` file was committed to the repository and contained environment values, including a password-like value. This violates safe secret handling and the task requirement that `.env` must not appear in the repository.
- Fix: Removed `api/.env` from version control, added `.gitignore`, and added a root `.env.example` with placeholder values only.

## 2. Missing `.gitignore`

- File: `.gitignore`
- Line: 1-11
- Problem: The project had no `.gitignore`, which allowed accidental commits of `.env`, caches, virtual environments, coverage outputs, and dependency folders.
- Fix: Added `.gitignore` to exclude `.env`, `node_modules`, Python cache files, coverage files, and local virtual environment directories.

## 3. Missing example environment file

- File: `.env.example`
- Line: 1-9
- Problem: The repository did not provide a safe example file for required environment variables.
- Fix: Added `.env.example` with placeholder values for all required variables used by the services and Docker Compose.

## 4. Frontend used hardcoded API URL

- File: `frontend/app.js`
- Line: 6
- Problem: The frontend used `http://localhost:8000`, which breaks container-to-container communication because `localhost` inside a container refers to the container itself.
- Fix: Replaced the hardcoded URL with `process.env.API_URL || "http://api:8000"`.

## 5. Frontend used hardcoded port

- File: `frontend/app.js`
- Line: 7
- Problem: The frontend listened on a fixed port instead of using environment-driven configuration.
- Fix: Added `FRONTEND_PORT` support with `process.env.FRONTEND_PORT || 3000`.

## 6. Frontend had no health endpoint

- File: `frontend/app.js`
- Line: 12-14
- Problem: The frontend had no dedicated health route, making Docker health checks impossible.
- Fix: Added `/health` endpoint returning HTTP 200 and `{ "status": "ok" }`.

## 7. Frontend listen block was hardcoded

- File: `frontend/app.js`
- Line: 29-31
- Problem: The server startup used a fixed port and logged a fixed value.
- Fix: Updated the listen block to use the configured `PORT`.

## 8. Frontend was missing lint tooling

- File: `frontend/package.json`
- Line: 5-6, 11-13
- Problem: The frontend had no lint script and no ESLint dependency, which would fail the CI lint requirement.
- Fix: Added `lint` script and installed ESLint as a dev dependency.

## 9. Frontend had no ESLint configuration

- File: `frontend/eslint.config.js`
- Line: 1-16
- Problem: ESLint was added but no config existed, so linting would not run reliably.
- Fix: Added an ESLint flat config for the frontend codebase.

## 10. API used hardcoded Redis connection values

- File: `api/main.py`
- Line: 7-14
- Problem: The API originally connected to Redis using hardcoded `localhost` and `6379`, which fails in Docker and ignores environment configuration.
- Fix: Replaced hardcoded values with `REDIS_HOST`, `REDIS_PORT`, `REDIS_PASSWORD`, and `QUEUE_NAME` environment variables.

## 11. API had no health endpoint

- File: `api/main.py`
- Line: 17-22
- Problem: The API had no health route for Docker health checks and dependency validation.
- Fix: Added `/health` endpoint that pings Redis and returns HTTP 503 if Redis is unavailable.

## 12. API used hardcoded queue name

- File: `api/main.py`
- Line: 26
- Problem: The queue name was hardcoded as `"job"`.
- Fix: Replaced the hardcoded queue name with configurable `QUEUE_NAME`.

## 13. API returned improper not-found response

- File: `api/main.py`
- Line: 32-33
- Problem: Missing jobs returned a plain JSON error instead of an HTTP 404 response.
- Fix: Replaced the plain return value with `HTTPException(status_code=404, detail="Job not found")`.

## 14. API runtime and dev dependencies were mixed together

- File: `api/requirements.txt`
- Line: 1-3
- Problem: Runtime, test, and lint dependencies were mixed in a way that would install unnecessary tools into the production image.
- Fix: Split dependencies into `requirements.txt` for runtime and `requirements-dev.txt` for test/lint tools.

## 15. API had no test coverage

- File: `api/tests/test_main.py`
- Line: 1-42
- Problem: The starter repository had no unit tests for the API.
- Fix: Added unit tests for job creation, job lookup success, job lookup failure, and API health check using mocked Redis.

## 16. API package import path was fragile for testing

- File: `api/__init__.py`
- Line: 1
- Problem: The `api` folder was not an explicit package, which could make CI test imports unreliable.
- Fix: Added `api/__init__.py`.

## 17. Python lint config was missing

- File: `api/.flake8`
- Line: 1-3
- Problem: There was no Python lint configuration for CI.
- Fix: Added `.flake8` with a line length limit and common excludes.

## 18. Worker used hardcoded Redis connection values

- File: `worker/worker.py`
- Line: 6-15
- Problem: The worker also used hardcoded `localhost` and `6379`, which would fail inside containers.
- Fix: Replaced the Redis connection with environment-driven configuration.

## 19. Worker used hardcoded processing settings

- File: `worker/worker.py`
- Line: 10
- Problem: Job processing delay was hardcoded and not configurable.
- Fix: Added `PROCESSING_DELAY` environment variable.

## 20. Worker had no graceful shutdown handling

- File: `worker/worker.py`
- Line: 17-23
- Problem: The worker ran in an endless loop without proper signal-based shutdown behavior.
- Fix: Added SIGINT and SIGTERM handlers and a `running` flag for graceful shutdown.

## 21. Worker had no error handling around queue processing

- File: `worker/worker.py`
- Line: 30-39
- Problem: Failures in Redis operations or processing could crash the worker immediately.
- Fix: Wrapped the main loop in `try/except` blocks for Redis and unexpected errors.

## 22. Worker dependency was unpinned

- File: `worker/requirements.txt`
- Line: 1
- Problem: The worker dependency was not pinned, reducing reproducibility.
- Fix: Pinned `redis==5.0.8`.

## 23. Missing API Dockerfile

- File: `api/Dockerfile`
- Line: 1-18
- Problem: The API was not containerized.
- Fix: Added a production-oriented Dockerfile using a slim Python base image, non-root user, health check, and runtime-only dependencies.

## 24. Missing worker Dockerfile

- File: `worker/Dockerfile`
- Line: 1-15
- Problem: The worker was not containerized.
- Fix: Added a Dockerfile with a non-root user, Redis-based health check, and runtime-only dependency install.

## 25. Missing frontend Dockerfile

- File: `frontend/Dockerfile`
- Line: 1-18
- Problem: The frontend was not containerized.
- Fix: Added a Dockerfile using Node Alpine, non-root user, production dependency install, and health check.

## 26. Missing Compose orchestration

- File: `docker-compose.yml`
- Line: 1-55
- Problem: The starter repo had no multi-service orchestration for the full stack.
- Fix: Added `docker-compose.yml` to run frontend, API, worker, and Redis together.

## 27. Redis was not explicitly protected from host exposure

- File: `docker-compose.yml`
- Line: 2-15
- Problem: Redis needed to remain internal-only.
- Fix: Configured Redis without host port publishing and attached it only to the internal network.

## 28. Service startup order was not health-based

- File: `docker-compose.yml`
- Line: 19-21, 35-37, 49-51
- Problem: Services needed to wait for healthy dependencies, not just started containers.
- Fix: Added `depends_on` conditions using `service_healthy`.

## 29. Compose environment variables were incomplete

- File: `docker-compose.yml`, `.env.example`
- Line: multiple
- Problem: The stack required environment-driven configuration for ports and service communication.
- Fix: Added env-based configuration for API port, frontend port, Redis settings, queue name, and processing delay.

## 30. CPU and memory limits were missing

- File: `docker-compose.yml`
- Line: 13-14, 29-30, 44-45, 59-60
- Problem: The task required resource limits for every service.
- Fix: Added CPU and memory limits for Redis, API, worker, and frontend.

## 31. CI/CD pipeline was missing

- File: `.github/workflows/ci-cd.yml`
- Line: 1 onward
- Problem: The starter repo had no GitHub Actions pipeline.
- Fix: Added a staged CI/CD workflow implementing `lint`, `test`, `build`, `security-scan`, `integration-test`, and `deploy` in strict order.

## 32. CI lint stage was missing Dockerfile linting

- File: `.github/workflows/ci-cd.yml`
- Line: 31-36
- Problem: The task requires Dockerfile linting with Hadolint.
- Fix: Added Hadolint installation and Dockerfile lint execution.

## 33. CI test stage was missing coverage artifact upload

- File: `.github/workflows/ci-cd.yml`
- Line: 52-57
- Problem: The task requires test coverage to be generated and uploaded.
- Fix: Added pytest coverage generation and artifact upload.

## 34. CI build stage was missing local registry publishing

- File: `.github/workflows/ci-cd.yml`
- Line: 59-91
- Problem: The task requires images to be built, tagged, and pushed to a local registry service in the workflow.
- Fix: Added a registry service and image build/push steps for API, worker, and frontend.

## 35. CI security scan stage was missing

- File: `.github/workflows/ci-cd.yml`
- Line: 92-147
- Problem: The task requires image scanning with Trivy and SARIF artifact upload.
- Fix: Added Trivy scanning for all built images, failing on `CRITICAL`, with SARIF artifact upload.

## 36. CI integration test stage was missing

- File: `.github/workflows/ci-cd.yml`
- Line: 149-194
- Problem: The task requires full-stack integration testing through the frontend.
- Fix: Added a job that creates a temporary `.env`, starts the stack, submits a job through the frontend, polls until completion, and tears the stack down.

## 37. CI deploy stage did not exist

- File: `.github/workflows/ci-cd.yml`
- Line: 196-255
- Problem: The task requires a deploy stage that runs only on `main` and validates health before replacement.
- Fix: Added a deploy job gated to pushes on `main`, with candidate API validation, final API re-check, and stack health confirmation.

## 38. Hardcoded password in workflow YAML

- File: `.github/workflows/ci-cd.yml`
- Line: integration and deploy env creation steps
- Problem: Embedding a literal password in workflow YAML violates the task rule against hardcoded passwords.
- Fix: Replaced the hardcoded value with `${{ secrets.REDIS_PASSWORD }}`.

## 39. Repository documentation was incomplete

- File: `README.md`
- Line: 1 onward
- Problem: The original README contained only the project title and did not explain setup, usage, environment configuration, verification steps, or the CI/CD pipeline.
- Fix: Rewrote the README with prerequisites, environment setup, Docker commands, startup verification, local checks, architecture summary, and pipeline overview.