# Story 1.1: Project Scaffolding & Monorepo Setup

## Status: Draft

## Story

- As a Platform/DevOps Engineer (or a Developer Agent setting up the project)
- I want to establish the initial project scaffolding and monorepo structure
- so that both frontend and backend development can begin in an organized, standardized, and manageable way.

## Acceptance Criteria (ACs)

1. A new Git repository is initialized for the project (e.g., on GitHub).
2. A top-level monorepo structure is created with at least `frontend/` and `backend/` directories.
3. A basic root `README.md` file is created with a project title and a brief description.
4. A comprehensive `.gitignore` file is created at the root, suitable for a Python/Node.js monorepo (ignoring common OS files, IDE files, virtual environments, `node_modules`, build artifacts, `.env` files, etc.).

## Tasks / Subtasks

- [ ] Task 1: Initialize Git Repository (AC: #1)
  - [ ] Create a new repository on the chosen Git hosting service (e.g., GitHub).
  - [ ] Clone the empty repository locally (if applicable).
- [ ] Task 2: Create Monorepo Directory Structure (AC: #2)
  - [ ] Create the root project folder (e.g., `mailchimp-trends-engine`).
  - [ ] Inside the root folder, create `backend/` directory.
  - [ ] Inside the root folder, create `frontend/` directory.
  - [ ] Inside the root folder, create `docs/` directory and populate it with the existing PRD, architecture, and UI/UX spec documents.
  - [ ] Inside the root folder, create `.github/workflows/` directories.
  - [ ] Inside the root folder, create `kubernetes/` directory.
- [ ] Task 3: Create Initial Root `README.md` (AC: #3)
  - [ ] Create `README.md` in the project root.
  - [ ] Add the project title (e.g., "# Mailchimp Marketing Trends Engine (MVP)").
  - [ ] Add a brief one-paragraph project description based on `prd.md` (Section 1 "Goal, Objective and Context").
- [ ] Task 4: Create Root `.gitignore` File (AC: #4)
  - [ ] Create `.gitignore` in the project root.
  - [ ] Add common ignore patterns for Python (e.g., `__pycache__/`, `*.pyc`, `*.pyo`, `*.pyd`, `.Python`, `env/`, `venv/`, `ENV/`, `*.egg-info/`, `.pytest_cache/`, `.mypy_cache/`, `.ruff_cache/`).
  - [ ] Add common ignore patterns for Node.js (e.g., `node_modules/`, `*.log`, `build/`, `dist/`, `.pnp.*`).
  - [ ] Add common ignore patterns for IDEs (e.g., `.vscode/`, `.idea/`).
  - [ ] Add common ignore patterns for OS files (e.g., `.DS_Store`, `Thumbs.db`).
  - [ ] Add ignore patterns for environment files (e.g., `.env`, `.env.*`, `!*.env.example`, `!*.env.local.example`).
  - [ ] Add ignore patterns for local SQLite database files (e.g., `*.db`, `*.sqlite3`).
- [ ] Task 5: Initial Commit
  - [ ] Stage all created files and directories.
  - [ ] Make an initial Git commit with a message like "feat: Initial project scaffolding and monorepo structure (Story 1.1)".
  - [ ] Push the initial commit to the remote repository (if applicable).

## Dev Technical Guidance

- **Monorepo Tooling (Future Consideration):** For this initial setup, direct directory creation is sufficient. `pnpm` workspaces will be configured in a later story (`pnpm-workspace.yaml`) for frontend, and `Hatch` will manage the backend within its directory. No root-level monorepo management tool (like Turborepo or Nx) is planned for MVP setup simplicity.
- **`.gitignore` Content:** Refer to standard `.gitignore` templates for Python and Node.js projects (e.g., from [github/gitignore](https://github.com/github/gitignore)) as a base and customize as needed for this specific monorepo setup. Ensure it covers outputs from linters, type checkers, and test runners.
- **`docs/` Directory:** Ensure all provided specification documents (`prd.md`, `architecture.md`, `frontend-architecture.md`, `ui-ux-spec.md`, related images, and PDF guides) are placed in the `docs/` directory (potentially in subdirectories like `docs/assets/` for images/PDFs if desired for organization).
- **File Encoding:** Ensure all text files are UTF-8 encoded.

## Story Progress Notes

### Completion Notes List

{Any notes about implementation choices, difficulties, or follow-up needed}

### Change Log

2025-05-17 - Kayvan Sylvan - Story Drafted
