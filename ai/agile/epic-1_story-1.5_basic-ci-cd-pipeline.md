# Story 1.5: Basic CI/CD Pipeline with Build & Linting (using `pnpm`)

## Status: Draft

## Story

- As a DevOps Engineer (or a Developer Agent responsible for CI/CD)
- I want to establish a basic CI/CD pipeline using GitHub Actions that automates building and linting for both frontend and backend applications
- so that code quality is maintained, integration issues are caught early, and build artifacts (Docker images) are consistently produced.

## Acceptance Criteria (ACs)

1. A GitHub Actions workflow file (e.g., `tests.yml` or `ci.yml`) is created in `.github/workflows/`.
2. The workflow is triggered on pushes to `develop` and `main` branches, and on pull requests targeting `develop` and `main`.
3. The workflow checks out the repository code.
4. The workflow includes a job for backend checks:
    - [ ] Sets up the correct Python version (e.g., 3.13.3 using `actions/setup-python`).
    - [ ] Installs `uv`.
    - [ ] Sets up the backend environment and installs dependencies using `uv sync` (potentially via `backend/bootstrap/setup.sh` or Makefile target).
    - [ ] Runs backend linters (Ruff, Pylint) successfully (e.g., via `backend/Makefile` target `lint`).
    - [ ] Builds the backend Docker image successfully (e.g., via `backend/Makefile` target `build` or direct Docker commands).
5. The workflow includes a job for frontend checks:
    - [ ] Sets up the correct Node.js version (e.g., 22.x using `actions/setup-node`).
    - [ ] Installs `pnpm`.
    - [ ] Installs frontend dependencies using `pnpm install --frozen-lockfile`.
    - [ ] Runs frontend linters (ESLint, Prettier) successfully (e.g., via `pnpm lint` script in `frontend/package.json`).
    - [ ] Builds the frontend Docker image successfully (e.g., via `frontend/Dockerfile` and Docker commands).
6. The CI pipeline fails if any linting step fails for backend or frontend.
7. The CI pipeline fails if any Docker image build step fails for backend or frontend.
8. (Optional but Recommended) The workflow caches dependencies (Python packages via `uv` cache, Node modules via `pnpm` cache) to speed up subsequent runs.

## Tasks / Subtasks

- [ ] Task 1: Design GitHub Actions Workflow Structure (AC: #1, #2)
  - [ ] Create `.github/workflows/ci.yml` (or `tests.yml`).
  - [ ] Define triggers: `on: [push: { branches: [main, develop] }, pull_request: { branches: [main, develop] }]`.
  - [ ] Define jobs structure (e.g., `backend-checks`, `frontend-checks`). Consider if they can run in parallel.
- [ ] Task 2: Implement Backend Checks Job (AC: #3, #4, #6, #7, #8)
  - [ ] In the `backend-checks` job:
    - [ ] Use `actions/checkout@v4` (or latest).
    - [ ] Use `actions/setup-python@v5` (or latest) with the project's Python version.
    - [ ] Add step to install `uv` (e.g., `pip install uv` or pre-built action if available).
    - [ ] Add step to cache `uv` global packages if applicable.
    - [ ] Run backend dependency installation (e.g., `cd backend && sh bootstrap/setup.sh` or `cd backend && make setup`).
    - [ ] Add step to run backend linters (e.g., `cd backend && make lint`).
    - [ ] Add step to build backend Docker image (e.g., `cd backend && make build` or `docker build -f backend/Dockerfile -t backend-temp ./backend`).
- [ ] Task 3: Implement Frontend Checks Job (AC: #3, #5, #6, #7, #8)
  - [ ] In the `frontend-checks` job:
    - [ ] Use `actions/checkout@v4`.
    - [ ] Use `pnpm/action-setup@v4` (or latest) to install `pnpm`.
    - [ ] Use `actions/setup-node@v4` with Node.js 22.x and specify `cache: 'pnpm'` and `cache-dependency-path: 'frontend/pnpm-lock.yaml'`.
    - [ ] Run frontend dependency installation (e.g., `cd frontend && pnpm install --frozen-lockfile`).
    - [ ] Add step to run frontend linters (e.g., `cd frontend && pnpm lint`).
    - [ ] Add step to build frontend Docker image (e.g., `docker build -f frontend/Dockerfile -t frontend-temp ./frontend`).
- [ ] Task 4: Configure Job Failure Behavior (AC: #6, #7)
  - [ ] Ensure that if any linting or build step fails, the respective job and the overall workflow fail. This is default behavior for script steps in GitHub Actions.
- [ ] Task 5: Test CI Pipeline
  - [ ] Create a temporary branch and push changes to trigger the workflow.
  - [ ] Introduce a temporary linting error to verify failure.
  - [ ] Introduce a temporary build error (e.g., in a Dockerfile) to verify failure.
  - [ ] Ensure successful runs pass all steps.
  - [ ] Merge the workflow file into `develop` branch via PR.

## Dev Technical Guidance

- **GitHub Actions Workflow Syntax:** Refer to official GitHub Actions documentation for syntax on workflows, jobs, steps, `actions/checkout`, `actions/setup-python`, `actions/setup-node`, `pnpm/action-setup`.
- **Dependency Caching:**
  - For Python with `uv`: `uv` has its own caching mechanism. Check `uv` documentation for CI caching recommendations or use generic `actions/cache` if needed for the `uv` environment itself.
  - For Node.js with `pnpm`: `actions/setup-node` with `cache: 'pnpm'` and `cache-dependency-path` is the standard way.
- **Makefile/Script Usage:** Leverage the Makefiles (`backend/Makefile`) and `pnpm` scripts (`frontend/package.json`) created in previous stories for running linters and builds within the CI steps. This promotes consistency between local dev and CI.
  - Example step: `run: cd backend && make lint`
  - Example step: `run: cd frontend && pnpm lint`
- **Docker Builds in CI:** Ensure Docker is available in the GitHub Actions runner environment (usually is). The build commands should be straightforward. Tagging images with `temp` or similar is fine as these CI builds are primarily for validation, not pushing to a registry in this story.
- **Workflow File Location:** Place the workflow YAML file in `.github/workflows/`. Name it descriptively, e.g., `ci-checks.yml` or `main-pipeline.yml`.
- **Parallel Jobs:** Backend and frontend checks can often run in parallel to speed up the CI process. Define them as separate jobs that don't depend on each other.

## Story Progress Notes

### Completion Notes List

{Any notes about implementation choices, difficulties, or follow-up needed}

### Change Log

2025-05-17 - Kayvan Sylvan - {Description of Change, e.g., "Story Drafted"}
