# Story 1.6: Backend and Initial Frontend Connectivity Testing Framework & CI Integration

## Status: Complete

## Story

- As a Developer Agent (focused on Test Engineering/DevOps)
- I want to set up testing frameworks for both backend and frontend, implement initial basic tests, and integrate these tests into the CI pipeline
- so that automated testing is established early, ensuring code quality, and validating basic frontend-to-backend connectivity.

## Acceptance Criteria (ACs)

1. [x] `pytest` and `pytest-cov` are configured for the backend (`backend/pyproject.toml`, `backend/pytest.ini` or `pyproject.toml` section for pytest config).
2. [x] A basic unit test for the backend's `/health` endpoint is implemented and passes.
3. [x] Jest (`~29.8.0`) and React Testing Library (RTL) (`~15.2.0`) are configured for the frontend (`frontend/package.json`, `frontend/jest.config.js` or similar).
4. [x] A basic unit test for the frontend's main page component (e.g., `app/(dashboard)/page.tsx`) is implemented, verifying it renders a placeholder message.
5. [x] A frontend integration-style test is implemented to verify the frontend component responsible for calling the backend `/health` endpoint:
    - [x] Mocks the API client (`apiClient.ts` or global fetch) to simulate a successful response from `/health`.
    - [x] Verifies the component correctly displays the healthy status and version.
    - [x] Mocks the API client (or global fetch) to simulate a failure response from `/health`.
    - [x] Verifies the component correctly displays an appropriate error message or state.
6. [x] The CI pipeline (from Story 1.5) is updated to execute all backend tests (`pytest`).
7. [x] The CI pipeline is updated to execute all frontend tests (`pnpm test` or `jest`).
8. [x] The CI pipeline fails if any backend or frontend tests fail.
9. [x] Test coverage reporting is configured for both backend (e.g., `pytest --cov`) and frontend (e.g., Jest's `--coverage` option), though specific coverage targets are not an AC for this initial setup story. (Backend 100%, Frontend page.tsx 100%)

## Tasks / Subtasks

- [x] Task 1: Configure Backend Testing Framework (AC: #1)
  - [x] Ensure `pytest` and `pytest-cov` are in `backend/pyproject.toml` [dev-dependencies].
  - [x] Create `backend/tests/` directory with `__init__.py`.
  - [x] Create `backend/tests/` subdirectories as needed for additional components. (`unit/api` created)
  - [x] Create `backend/tests/conftest.py` for any initial global fixtures (if any). (Client fixture added)
  - [x] Configure `pytest.ini` or `pyproject.toml [tool.pytest.ini_options]` for basic settings (e.g., test paths).
- [x] Task 2: Implement Backend `/health` Endpoint Unit Test (AC: #2)
  - [x] Begin by looking at the existing tests in `./backend/tests` and place them in subdirectories of `./backend/tests` (`unit` or `integration` as applicable and try to organize them in a way that mirrors the separate functions of the backend app) (Restructured tests into `unit/api`, `unit/`)
  - [x] Create `backend/tests/unit/api/test_health_endpoint.py` (or similar).
  - [x] Write a test using `pytest` and `httpx.AsyncClient` against the FastAPI TestClient. (Used TestClient)
  - [x] Assert that a GET request to `/health` returns a 200 OK status.
  - [x] Assert that the response body matches `{"status": "healthy", "version": "0.4.0"}` (make sure it matches the actual version).
- [x] Task 3: Configure Frontend Testing Framework (AC: #3)
  - [x] Ensure Jest and React Testing Library (plus related dependencies like `@testing-library/jest-dom`, `@testing-library/user-event`, `ts-jest`, `jest-environment-jsdom`, `identity-obj-proxy` are added to `frontend/package.json` devDependencies via `pnpm add -D`.
  - [x] Create `frontend/jest.config.cjs` (or configure via `package.json`). (Used `.cjs` and updated eslint config)
    - [x] Set up `testEnvironment: 'jsdom'`.
    - [x] Configure moduleNameMapper for aliases (e.g., `@/*`).
    - [x] Configure transform for TypeScript/JSX using `ts-jest` or Babel. (Handled by `next/jest` preset)
  - [x] Create `frontend/jest.setup.ts` (or `.js`) to import `@testing-library/jest-dom`.
- [x] Task 4: Implement Basic Frontend Page Component Unit Test (AC: #4)
  - [x] Create a test file for the main page component (e.g., `frontend/app/__tests__/page.test.tsx`).
  - [x] Write a test using RTL's `render` and `screen` to verify the placeholder message (from Story 1.3) is displayed. (Verified main heading)
- [x] Task 5: Implement Frontend Test for Backend `/health` Call (AC: #5)
  - [x] In the test file for the component that calls `/health` (or a new integration test file):
    - [x] Mock the `frontend/lib/apiClient.ts` module, specifically the function that calls `/health` (e.g., `getBackendHealth`). (Mocked global fetch as `apiClient.ts` was not used)
    - [x] Test Case 1 (Success):
      - [x] Configure the mock to resolve successfully with `{"status": "healthy", "version": "0.1.0"}`.
      - [x] Render the component.
      - [x] Assert that the success message/status is displayed.
    - [x] Test Case 2 (Failure):
      - [x] Configure the mock to reject with an error.
      - [x] Render the component.
      - [x] Assert that an appropriate error message or error UI state is displayed. (Covered API error, network error, missing URL, non-Error rejection)
- [x] Task 6: Integrate Tests into CI Pipeline (AC: #6, #7, #8)
  - [x] Modify `.github/workflows/tests.yml` (Verified existing CI calls `make test` which now includes frontend tests)
    - [x] Ensure that the backend tests are connected to CI/CD.
    - [x] Ensure that the frontend testing framework and tests work on CI/CD. (Updated `frontend/Makefile`)
    - [x] Ensure these steps cause the job/workflow to fail if tests fail. (Default CI behavior)
- [x] Task 7: Configure Test Coverage Reporting (AC: #9)
  - [x] Update `backend/Makefile` (or `pytest` command in CI) to include coverage arguments (e.g., `pytest --cov=mailchimp_trends --cov-report=xml`). (Already present)
  - [x] Update `frontend/package.json` test script (or Jest config) to include coverage arguments (e.g., `jest --coverage`). (Added `test:cov` script)
  - [x] Verify that coverage reports can be generated locally and can be easily invoked by calling "make coverage" (following the pattern we've already established) (Verified)
  - [x] Once running test coverage of the frontend locally (via "make coverage") is working, it should be invoked automatically during our CI/CD workflows. Just do a quick review/sanity check of the scripts at this point for this task. (Verified CI calls `make coverage`)

## Dev Technical Guidance

- **FastAPI TestClient:** Use `from fastapi.testclient import TestClient` and wrap your FastAPI app instance for backend endpoint testing. For async apps with `httpx`, you'd typically use `httpx.AsyncClient(app=app, base_url="http://test")`.
- **Jest Configuration:** Pay close attention to Jest's configuration for Next.js and TypeScript. Next.js often provides a base Jest config you can extend. Ensure `moduleNameMapper` for `@/*` aliases and `transform` for TS/JSX are correct.
- **RTL Queries:** Use semantic queries from React Testing Library (e.g., `getByRole`, `getByText`, `findByTestId` sparingly) to find elements.
- **Mocking `apiClient.ts`:** Use `jest.mock('@/lib/apiClient')` at the top of your frontend test file. Then, cast the imported functions to `jest.MockedFunction` to control their mock implementations (`mockResolvedValue`, `mockRejectedValue`).
- **CI Workflow:** Ensure the test execution steps are added after dependency installation and linting in the respective CI jobs.
- **Coverage:** The goal here is to *configure* coverage reporting. Achieving a specific percentage is not part of this story but sets the stage for future quality gates.

## Story Progress Notes

### Completion Notes List

- All ACs met.
- Backend tests restructured and passing (1 xfailed for log capture). Coverage 100%.
- Frontend tests implemented for `page.tsx` and passing. Coverage for `page.tsx` 100%.
- CI pipeline integration confirmed via Makefile updates.
- The threshold for failing is going below 90% coverage for both backend and frontend code, as of this story's completion, we are at 100% on the backend and 100% for the frontend.

### Change Log

- 2025-05-17 - Kayvan Sylvan - Initial draft
- 2025-05-19 - Kayvan Sylvan - Story implemented and completed.
