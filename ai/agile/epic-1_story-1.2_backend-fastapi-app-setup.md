# Story 1.2: Backend "Majestic Monolith" (FastAPI) Application Setup

## Status: Complete

## Story

- As a Backend Developer
- I want to set up the foundational FastAPI application structure for the backend
- so that core backend functionalities, API endpoints, and business logic can be developed in an organized, scalable, and maintainable manner, adhering to the "Majestic Monolith" pattern.

## Acceptance Criteria (ACs)

1. A Python virtual environment is created and managed using `uv` (as per `architecture.md`).
2. A `pyproject.toml` file is configured for the backend project using `Hatch` as the build system, defining project metadata and core dependencies (e.g., `fastapi`, `uvicorn`, `httpx`, `pytest`).
3. The backend source code is organized under `backend/app//` with initial subdirectories for `api/`, `core/`, `db/`, `schemas/` and a `main.py` as per `architecture.md` ("Project Structure" and "Component View").
4. A basic FastAPI application is initialized in `backend/app//main.py`.
5. A simple `/health` API endpoint is implemented in the FastAPI application that returns a JSON response like `{"status": "healthy", "version": "x.y.z"}` (version can be hardcoded initially, e.g., "0.1.0").
6. A `Dockerfile` is created in the `backend/` directory to containerize the FastAPI application.
7. The Docker image for the backend application can be built successfully.
8. The containerized backend application can be run locally (e.g., via Docker command or eventually via k3s from Story 1.4), and the `/health` endpoint is accessible and returns the correct response.
9. A `backend/Makefile` includes targets for common development tasks like `lint`, `test`, `run` (local dev server), `build` (Docker image).
10. Initial linter configurations (`.ruff.toml`, `.pylintrc`) are added to `backend/`, and the initial code passes linting checks.
11. A `.python-version` file is added to `backend/` specifying the target Python version (e.g., 3.13.3).
12. `uv` is used for dependency installation and environment synchronization (`uv sync`). A `backend/bootstrap/setup.sh` script may be provided to streamline initial `uv` environment setup.

## Tasks / Subtasks

- [x] Task 1: Initialize Python Environment and Package Management (AC: #1, #2, #11, #12)
  - [x] Create `backend/.python-version` file with content `3.13.3`.
  - [x] Initialize `uv` environment within `backend/` (e.g., `uv init`).
  - [x] Initialize `backend/pyproject.toml` for `Hatch`.
    - [x] Define project metadata (name: `mailchimp-trends-backend`, version: `0.1.0`).
    - [x] Specify dependencies: `fastapi`, `uvicorn[standard]`, `httpx`, `python-dotenv`.
    - [x] Specify dev dependencies: `pytest`, `pytest-cov`, `ruff`, `pylint`.
  - [x] Hook up bootstrap commands - so that "make bootstrap" will set up backend.
  - [x] Ensure dependencies can be installed using `uv sync`.
- [x] Task 2: Create Backend Application Directory Structure (AC: #3)
  - [x] Create `backend/src/app/`.
  - [x] Create `backend/src/app/__init__.py`.
  - [x] Create other source and test files as needed.
- [x] Task 3: Implement Basic FastAPI Application & Health Endpoint (AC: #4, #5)
  - [x] In `backend/app/server.py`, import FastAPI.
  - [x] Create a FastAPI app instance.
  - [x] Implement a `GET /health` endpoint.
    - [x] Define a Pydantic response model for health status (e.g., in `schemas/health.py`). (Implicitly handled by FastAPI's default JSON response for dicts; specific schema file not created yet but can be added if complex.)
    - [x] Return `{"status": "healthy", "version": "0.1.0"}`.
- [x] Task 4: Create Backend Dockerfile (AC: #6)
  - [x] Create `backend/Dockerfile`.
  - [x] Use an appropriate Python base image (e.g., `python:3.13-slim`).
  - [x] Set up a non-root user.
  - [x] Copy `pyproject.toml` (and `uv.lock` if generated and used).
  - [x] Install dependencies using `uv sync --no-cache --frozen`. (Corrected from --dev)
  - [x] Copy the `backend/app/` directory into the image.
  - [x] Expose the application port (e.g., 8000).
  - [x] Set the `CMD` to run the application using `uvicorn`.
- [x] Task 5: Configure Linters (AC: #10)
  - [x] Create `.ruff.toml` with basic configuration (e.g., line length, select rules based on `architecture.md`).
  - [x] Create `.pylintrc` with basic configuration.
  - [x] Ensure initial code passes `ruff check .` and `pylint app/`. (Corrected path for pylint)
- [x] Task 6: Create Backend Makefile (AC: #9)
  - [x] Create `backend/Makefile`.
  - [x] Add target `lint`: runs `ruff format . --check`, `ruff check .`, and `pylint .`. (Corrected pylint path)
  - [x] Add target `test`: runs `pytest`.
  - [x] Add target `run`: starts the dev server using `uvicorn app.server:app --reload --host 0.0.0.0 --port 8000`. (Corrected app path)
  - [x] Add target `docker-build`: builds the Docker image (e.g., `docker build -t mailchimp-trends-backend:latest .`). (Renamed from `build` for clarity and updated command)
- [x] Task 7: Verify Docker Build and Run (AC: #7, #8)
  - [x] Build the Docker image using the `Makefile` or Docker command.
  - [x] Run the container locally.
  - [x] Access the `/health` endpoint from a browser or `curl` to verify the response.

## Dev Technical Guidance

- **FastAPI App Initialization:** In `main.py`, ensure the FastAPI app instance is created. The health endpoint can be a simple function decorated with `@app.get("/health")`.
- **Uvicorn Command:** The `CMD` in Dockerfile should be `["uvicorn", "mailchimp_trends.main:app", "--host", "0.0.0.0", "--port", "8000"]`. The port 8000 is conventional for FastAPI apps.
- **`uv` for Dependencies in Docker:** The `uv pip compile` step is crucial if `requirements.txt` is preferred for Docker layers. If `uv` in the Docker image can efficiently install directly from `pyproject.toml` without a lock file, that could simplify it, but `requirements.txt` is a common pattern for Docker builds.
- **Pydantic Models for Schemas:** Even for the simple health check, defining a response model in `schemas/` (e.g., `schemas/health_schemas.py`) is good practice from the start.

    ```python
    # Example: backend/app//schemas/health_schemas.py
    from pydantic import BaseModel

    class HealthResponse(BaseModel):
        status: str
        version: str
    ```

- **Makefile Variables:** Use variables in the Makefile for image names, ports, etc., for easier modification.

- **Initial Linting:** Configure Ruff to be quite strict from the start to maintain code quality. `pylint` can supplement this.
- **`.env` file for Backend:** Create `backend/.env.example` with `BACKEND_VERSION="0.1.0"` and load it in `main.py` (e.g., using `python-dotenv` and Pydantic settings) to supply the version to the `/health` endpoint dynamically.

## Story Progress Notes

### Completion Notes List

### Change Log

- 2025-05-17 - Kayvan Sylvan - Initial draft
- 2025-05-19 - Kayvan Sylvan - Updated based on progress.
- 2025-05-19 - Kayvan Sylvan - Completed.
