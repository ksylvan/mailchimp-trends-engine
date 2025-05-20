# Story 4.4: Time-Series Visualization of Trend Evolution

## Status: Draft

## Story

- As a Frontend Developer
- I want to integrate a charting library to display a time-series visualization of a selected trend's evolution (e.g., score or mention frequency over time) in the "Trend Details Panel"
- so that users can visually understand the trajectory and significance of a trend, with the chart styled to align with Mailchimp's aesthetics.

## Acceptance Criteria (ACs)

1. A charting library (e.g., `Chart.js` with `react-chartjs-2`, or a lightweight alternative like `Recharts` if preferred and aligns with `shadcn/ui` style) is integrated into the frontend application.
2. The backend API (`/api/v1/trends/{trend_id}`) provides historical data points for a selected trend (e.g., an array of `{date, score, mention_frequency}` objects as per `TrendDetailResponse` in `architecture.md`).
3. When a trend is selected, the "Trend Details Panel" displays a time-series line chart showing the trend's score (or mention frequency) over time, based on the fetched historical data.
4. The chart is interactive (e.g., tooltips on hover showing data point values).
5. The chart is styled to align with Mailchimp's aesthetics as seen in `Final-Mailchimp-Aligned-Dashboard-Mockup.png` (e.g., using Cavendish Yellow for the primary data line, clean axes, legible labels, appropriate grid lines).
6. The chart component handles cases where historical data might be empty or insufficient for a meaningful chart (e.g., displays a "Not enough data to display chart" message).
7. The chart is reasonably responsive and adapts to the panel width.

## Tasks / Subtasks

- [ ] Task 1: Select and Integrate Charting Library (AC: #1)
  - [ ] Evaluate and choose a charting library. `Chart.js` (with `react-chartjs-2` wrapper) is a common choice. `Recharts` is another popular option. Consider ease of styling with Tailwind/CSS to match Mailchimp. *Decision: Use `Chart.js` with `react-chartjs-2` as it's versatile and generally straightforward to customize.*
  - [ ] Add `chart.js` and `react-chartjs-2` to `frontend/package.json` dependencies using `pnpm add`.
- [ ] Task 2: Prepare Backend API for Trend History (AC: #2)
  - [ ] This task is primarily on the **Backend**. Ensure the `/api/v1/trends/{trend_id}` endpoint in the FastAPI application returns a `history` array within `TrendDetailResponse`.
  - [ ] Each item in `history` should be like `{ date: "YYYY-MM-DDTHH:MM:SSZ", score: number, mention_frequency: number | null }`. This data comes from `TrendDataPointModel`.
- [ ] Task 3: Create Chart Component Wrapper (AC: #3, #5, #7)
  - [ ] Create `frontend/components/ui/TrendChart.tsx` (or similar).
  - [ ] This component will take `data: TrendDataPointSchema[]` (from `lib/types.ts`, aligning with `TrendDetailResponse.history`) as a prop.
  - [ ] Use `react-chartjs-2` (e.g., `<Line />` component) to render the chart.
  - [ ] Configure chart options:
    - **Data:** Map `TrendDataPointSchema[]` to Chart.js `datasets` (e.g., one dataset for 'score', potentially another for 'mention_frequency'). Use `date` for x-axis labels (time scale).
    - **Styling:**
      - Line color: Cavendish Yellow (`#FFE01B`) for the primary metric (e.g., score).
      - Grid lines: Subtle grey (`border-grey` or lighter).
      - Fonts for labels/tooltips: Helvetica Neue.
      - Remove unnecessary chart clutter (e.g., overly dense ticks, verbose legends if only one dataset).
    - **Responsiveness:** `maintainAspectRatio: false` is often useful for fitting charts into containers.
    - **Tooltips:** Enable default tooltips. Customize if needed.
- [ ] Task 4: Integrate Chart into `TrendDetailsPanel` (AC: #3, #6)
  - [ ] In `frontend/components/layout/TrendDetailsPanel.tsx`:
    - [ ] Import `TrendChart`.
    - [ ] When `selectedTrendDetails` (containing `history` data) is available and not empty:
      - [ ] Render `<TrendChart data={selectedTrendDetails.history} />`.
    - [ ] If `selectedTrendDetails.history` is empty or has too few points (e.g., < 2), display a message like "Not enough historical data to display chart."
    - [ ] Handle loading/error states for `selectedTrendDetails` before attempting to render the chart.
- [ ] Task 5: Ensure Chart Interactivity (AC: #4)
  - [ ] Verify that Chart.js default tooltips appear on hover over data points, showing the value.
- [ ] Task 6: Unit/Integration Tests for Chart Component and Panel
  - [ ] Test `TrendChart.tsx`:
    - [ ] Mock `react-chartjs-2` if direct rendering is complex in Jest, or test that data is passed correctly to it.
    - [ ] Test with empty data and with sample data.
  - [ ] Test `TrendDetailsPanel.tsx`:
    - [ ] Verify it renders the chart (or mock of it) when `selectedTrendDetails.history` has data.
    - [ ] Verify it shows the "Not enough data" message when history is empty/insufficient.

## Dev Technical Guidance

- **Chart.js Configuration:**
  - **Scales:** Configure time scale for the x-axis (`type: 'time'`) and linear scale for y-axis. Format date labels appropriately.
  - **Datasets:** Define `label`, `data` (array of y-values), `borderColor`, `backgroundColor` (for area under line if desired), `tension` (for line curve).
  - **Options:** Control aspects like tooltips, legend display, grid line visibility/color, aspect ratio, responsiveness.
  - Refer to `react-chartjs-2` and `Chart.js v3/v4` documentation.
- **Data Mapping:** The `history` array from `TrendDetailResponse` (which contains `TrendDataPointSchema` objects) needs to be mapped to the format Chart.js expects for its `labels` (x-axis) and `datasets.data` (y-axis).

    ```typescript
    // Example mapping for Chart.js
    // const chartData = {
    //   labels: history.map(p => new Date(p.date)), // Or pre-formatted date strings
    //   datasets: [
    //     {
    //       label: 'Trend Score',
    //       data: history.map(p => p.score),
    //       borderColor: '#FFE01B', // Cavendish Yellow
    //       tension: 0.1,
    //     },
    //   ],
    // };
    ```

- **Styling:** The chart in `Final-Mailchimp-Aligned-Dashboard-Mockup.png` is clean: yellow line, subtle x-axis labels (dates), y-axis score labels, minimal grid. Aim to replicate this.

- **Backend Data:** Ensure the backend provides enough historical data points in `TrendDataPointModel` for a meaningful chart. If only one data point exists, a line chart isn't useful.
- **`SelectedTrendContext`:** The `TrendDetailsPanel` will likely consume `SelectedTrendContext` (from `frontend-architecture.md`) to get the `selectedTrendDetails` object containing the `history` data.

## Story Progress Notes

### Completion Notes List

### Change Log

- 2025-05-17 - Kayvan Sylvan - Initial draft
