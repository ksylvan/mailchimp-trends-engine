# Story 1.6: Backend and Initial Frontend Connectivity Testing Framework & CI Integration

## Status: Draft

## Story

- As a Developer Agent (focused on Test Engineering/DevOps)
- I want to set up testing frameworks for both backend and frontend, implement initial basic tests, and integrate these tests into the CI pipeline
- so that automated testing is established early, ensuring code quality, and validating basic frontend-to-backend connectivity.

## Acceptance Criteria (ACs)

1. `pytest` and `pytest-cov` are configured for the backend (`backend/pyproject.toml`, `backend/pytest.ini` or `pyproject.toml` section for pytest config).
2. A basic unit test for the backend's `/health` endpoint is implemented and passes.
3. Jest (`~29.8.0`) and React Testing Library (RTL) (`~15.2.0`) are configured for the frontend (`frontend/package.json`, `frontend/jest.config.js` or similar).
4. A basic unit test for the frontend's main page component (e.g., `app/(dashboard)/page.tsx`) is implemented, verifying it renders a placeholder message.
5. A frontend integration-style test is implemented to verify the frontend component responsible for calling the backend `/health` endpoint:
    - [ ] Mocks the API client (`apiClient.ts`) to simulate a successful response from `/health`.
    - [ ] Verifies the component correctly displays the healthy status and version.
    - [ ] Mocks the API client to simulate a failure response from `/health`.
    - [ ] Verifies the component correctly displays an appropriate error message or state.
6. The CI pipeline (from Story 1.5) is updated to execute all backend tests (`pytest`).
7. The CI pipeline is updated to execute all frontend tests (`pnpm test` or `jest`).
8. The CI pipeline fails if any backend or frontend tests fail.
9. Test coverage reporting is configured for both backend (e.g., `pytest --cov`) and frontend (e.g., Jest's `--coverage` option), though specific coverage targets are not an AC for this initial setup story.

## Tasks / Subtasks

- [ ] Task 1: Configure Backend Testing Framework (AC: #1)
  - [ ] Ensure `pytest` and `pytest-cov` are in `backend/pyproject.toml` [dev-dependencies].
  - [ ] Create `backend/tests/` directory with `__init__.py`.
  - [ ] Create `backend/tests/unit/` and `backend/tests/integration/` subdirectories.
  - [ ] Create `backend/tests/conftest.py` for any initial global fixtures (if any).
  - [ ] Configure `pytest.ini` or `pyproject.toml [tool.pytest.ini_options]` for basic settings (e.g., test paths).
- [ ] Task 2: Implement Backend `/health` Endpoint Unit Test (AC: #2)
  - [ ] Create `backend/tests/unit/api/test_health_endpoint.py` (or similar).
  - [ ] Write a test using `pytest` and `httpx.AsyncClient` against the FastAPI TestClient.
  - [ ] Assert that a GET request to `/health` returns a 200 OK status.
  - [ ] Assert that the response body matches `{"status": "healthy", "version": "0.1.0"}` (or the configured version).
- [ ] Task 3: Configure Frontend Testing Framework (AC: #3)
  - [ ] Ensure Jest and React Testing Library (plus related dependencies like `@testing-library/jest-dom`, `@testing-library/user-event`, `ts-jest` or Babel config for TypeScript) are added to `frontend/package.json` devDependencies via `pnpm add -D`.
  - [ ] Create `frontend/jest.config.js` (or configure via `package.json`).
    - [ ] Set up `testEnvironment: 'jsdom'`.
    - [ ] Configure moduleNameMapper for aliases (e.g., `@/*`).
    - [ ] Configure transform for TypeScript/JSX using `ts-jest` or Babel.
  - [ ] Create `frontend/jest.setup.ts` (or `.js`) to import `@testing-library/jest-dom`.
- [ ] Task 4: Implement Basic Frontend Page Component Unit Test (AC: #4)
  - [ ] Create a test file for the main page component (e.g., `frontend/app/(dashboard)/__tests__/page.test.tsx`).
  - [ ] Write a test using RTL's `render` and `screen` to verify the placeholder message (from Story 1.3) is displayed.
- [ ] Task 5: Implement Frontend Test for Backend `/health` Call (AC: #5)
  - [ ] In the test file for the component that calls `/health` (or a new integration test file):
    - [ ] Mock the `frontend/lib/apiClient.ts` module, specifically the function that calls `/health` (e.g., `getBackendHealth`).
    - [ ] Test Case 1 (Success):
      - [ ] Configure the mock to resolve successfully with `{"status": "healthy", "version": "0.1.0"}`.
      - [ ] Render the component.
      - [ ] Assert that the success message/status is displayed.
    - [ ] Test Case 2 (Failure):
      - [ ] Configure the mock to reject with an error.
      - [ ] Render the component.
      - [ ] Assert that an appropriate error message or error UI state is displayed.
- [ ] Task 6: Integrate Tests into CI Pipeline (AC: #6, #7, #8)
  - [ ] Modify `.github/workflows/ci.yml` (or equivalent):
    - [ ] In the `backend-checks` job, add a step to run backend tests (e.g., `cd backend && make test` or `pytest`).
    - [ ] In the `frontend-checks` job, add a step to run frontend tests (e.g., `cd frontend && pnpm test`).
    - [ ] Ensure these steps cause the job/workflow to fail if tests fail.
- [ ] Task 7: Configure Test Coverage Reporting (AC: #9)
  - [ ] Update `backend/Makefile` (or `pytest` command in CI) to include coverage arguments (e.g., `pytest --cov=mailchimp_trends --cov-report=xml`).
  - [ ] Update `frontend/package.json` test script (or Jest config) to include coverage arguments (e.g., `jest --coverage`).
  - [ ] Verify that coverage reports can be generated locally (actual CI upload/processing of reports is optional for this story).

## Dev Technical Guidance

- **FastAPI TestClient:** Use `from fastapi.testclient import TestClient` and wrap your FastAPI app instance for backend endpoint testing. For async apps with `httpx`, you'd typically use `httpx.AsyncClient(app=app, base_url="http://test")`.
- **Jest Configuration:** Pay close attention to Jest's configuration for Next.js and TypeScript. Next.js often provides a base Jest config you can extend. Ensure `moduleNameMapper` for `@/*` aliases and `transform` for TS/JSX are correct.
- **RTL Queries:** Use semantic queries from React Testing Library (e.g., `getByRole`, `getByText`, `findByTestId` sparingly) to find elements.
- **Mocking `apiClient.ts`:** Use `jest.mock('@/lib/apiClient')` at the top of your frontend test file. Then, cast the imported functions to `jest.MockedFunction` to control their mock implementations (`mockResolvedValue`, `mockRejectedValue`).
- **CI Workflow:** Ensure the test execution steps are added after dependency installation and linting in the respective CI jobs.
- **Coverage:** The goal here is to *configure* coverage reporting. Achieving a specific percentage is not part of this story but sets the stage for future quality gates.

## Story Progress Notes

### Completion Notes List

{Any notes about implementation choices, difficulties, or follow-up needed}

### Change Log

- 2025-05-17 - Kayvan Sylvan - Initial draft
