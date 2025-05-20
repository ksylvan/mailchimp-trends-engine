# Story 4.5: Frontend Unit & Integration Tests for Dashboard Components

## Status: Draft

## Story

- As a Frontend Developer Agent
- I want to implement comprehensive unit and integration tests for the main dashboard components (Trend Feed Panel, Trend Details Panel, Trend Card, Filter Controls, Chart Wrapper)
- so that their individual functionality, interactions, and data handling are verified, ensuring a robust and reliable user interface.

## Acceptance Criteria (ACs)

1. Unit tests are created for the `TrendCard` component, covering rendering with different props, selection callback, and accessibility (as initiated in Story 4.2).
2. Unit tests are created for the `TrendFilterControls` component (from Story 4.3), verifying rendering of filter options and that `onFilterChange` callbacks are triggered correctly.
3. Unit tests are created for the `TrendChart` wrapper component (from Story 4.4), verifying it passes data correctly to the charting library and handles empty/insufficient data states. (Focus on the wrapper, not testing Chart.js itself).
4. Integration-style tests are created for the `TrendFeedPanel`, mocking API calls and context:
    - Verifies correct rendering of `TrendCard`s based on mock trend data.
    - Verifies that selecting a trend triggers the appropriate context update or callback.
    - Verifies that filter changes trigger API re-fetch logic (with mocked API).
5. Integration-style tests are created for the `TrendDetailsPanel`, mocking context:
    - Verifies correct display of trend details when `selectedTrendDetails` (from context) is populated.
    - Verifies chart (or chart wrapper) is rendered with history data.
    - Verifies "no data" or loading/error states are handled.
6. All new and existing frontend tests pass successfully.
7. The CI pipeline (from Story 1.6) executes these frontend tests.
8. Accessibility checks (`jest-axe`) are included in relevant component tests.

## Tasks / Subtasks

- [ ] Task 1: Finalize and Enhance `TrendCard` Unit Tests (AC: #1, #8)
  - [ ] Review and expand tests in `frontend/components/ui/__tests__/TrendCard.test.tsx`.
  - [ ] Ensure comprehensive coverage for prop variations, `onSelect` action, `isSelected` state, and keyboard interactions.
  - [ ] Confirm `jest-axe` checks are robust.
- [ ] Task 2: Implement `TrendFilterControls` Unit Tests (AC: #2, #8)
  - [ ] Create `frontend/features/trend-filtering/__tests__/TrendFilterControls.test.tsx` (or similar path).
  - [ ] Test rendering with various `categories` and `sentiments` props.
  - [ ] Mock `onFilterChange` and verify it's called with correct arguments when category `Select` value changes or sentiment `ToggleGroup`/`Button`s are interacted with.
  - [ ] Include `jest-axe` checks.
- [ ] Task 3: Implement `TrendChart` Unit Tests (AC: #3, #8)
  - [ ] Create `frontend/components/ui/__tests__/TrendChart.test.tsx`.
  - [ ] Test rendering with mock historical data, verifying that data is transformed and passed to `react-chartjs-2` Line component as expected (can mock the Line component itself to check props).
  - [ ] Test rendering with empty/insufficient data, verifying the "Not enough data" message appears.
  - [ ] Include `jest-axe` checks for the wrapper and any messages.
- [ ] Task 4: Implement `TrendFeedPanel` Integration Tests (AC: #4)
  - [ ] Create test file (e.g., `frontend/components/layout/__tests__/TrendFeedPanel.test.tsx`).
  - [ ] Mock `TrendsDataContext` to provide mock trend lists, filter state, and update functions.
  - [ ] Mock `SelectedTrendContext` (or the function to select a trend).
  - [ ] Mock `apiClient.getTrends` if the panel itself triggers fetches on filter changes.
  - [ ] Test that `TrendCard`s are rendered based on context data.
  - [ ] Test that interacting with `TrendFilterControls` (mocked or real if simple) triggers context updates and potentially `apiClient.getTrends`.
  - [ ] Test that clicking a `TrendCard` triggers the selection mechanism.
- [ ] Task 5: Implement `TrendDetailsPanel` Integration Tests (AC: #5)
  - [ ] Create test file (e.g., `frontend/components/layout/__tests__/TrendDetailsPanel.test.tsx`).
  - [ ] Mock `SelectedTrendContext` to provide various `selectedTrendDetails` states (loading, error, data present with history, data present without sufficient history).
  - [ ] Verify correct information (name, score, etc.) is displayed from context.
  - [ ] Verify `TrendChart` (or its mock) is rendered when history data is present.
  - [ ] Verify appropriate messages for loading, error, and "no chart data" states.
- [ ] Task 6: Ensure All Tests Pass and CI Integration (AC: #6, #7)
  - [ ] Run all frontend tests locally (`pnpm test --coverage` in `frontend/`) and ensure they pass.
  - [ ] Confirm that the CI pipeline executes these tests and fails on any test failure.

## Dev Technical Guidance

- **React Testing Library (RTL) Philosophy:** Focus on testing components from the user's perspective. Query by accessible roles, text, labels. Interact using `userEvent`.
- **Mocking Context:** For integration tests of panels, you'll need to wrap the component under test with a mock version of your Context Providers.

    ```typescript
    // Example for mocking context
    // import { render, screen } from '@testing-library/react';
    // import { TrendsDataContext } from '@/contexts/TrendsDataContext'; // Adjust path
    // import TrendFeedPanel from '@/components/layout/TrendFeedPanel'; // Adjust path

    // const mockTrendsContextValue = { /* ... mock state and functions ... */ };
    // render(
    //   <TrendsDataContext.Provider value={mockTrendsContextValue}>
    //     <TrendFeedPanel />
    //   </TrendsDataContext.Provider>
    // );
    ```

- **Mocking API Client:** As established in Story 1.6, use `jest.mock('@/lib/apiClient')` for mocking API calls made by components or contexts during tests.

- **`jest-axe`:** Use `const results = await axe(container); expect(results).toHaveNoViolations();` for accessibility checks.
- **Coverage:** Aim for good coverage of logic paths, prop variations, and interaction outcomes. While a specific percentage isn't an AC for this setup story, Story 1.6 configured coverage reporting.
- **Focus on Component Boundaries:** Unit tests should focus on individual components. Integration tests verify how a few closely related components work together, typically with their immediate dependencies (like context or API clients) mocked.

## Story Progress Notes

### Completion Notes List

### Change Log

- 2025-05-17 - Kayvan Sylvan - Initial draft
