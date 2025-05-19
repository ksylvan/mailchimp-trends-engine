# Story 4.2: Trend Display with Key Information

## Status: Draft

## Story

- As a Frontend Developer Agent
- I want to implement the `TrendCard` component and use it to display each identified marketing trend with its key information (name, date, sentiment, score) within the "Trend Feed Panel"
- so that users can quickly scan and identify relevant trends, with styling aligned to Mailchimp's aesthetics.

## Acceptance Criteria (ACs)

1. A reusable `TrendCard` React component is created (e.g., in `frontend/components/ui/TrendCard.tsx` or `frontend/components/layout/TrendCard.tsx` if specific to this layout panel).
2. The `TrendCard` component accepts a `trend` object (matching `TrendListItem` type from `lib/types.ts`) as a prop and displays its `name`, `identified_date` (formatted), `sentiment`, and `score`.
3. The `TrendFeedPanel` (from Story 4.1, or its content area) iterates over the list of fetched trends (from `apiClient.getTrends()`) and renders a `TrendCard` for each.
4. The `TrendCard` is styled to align with the "Final-Mailchimp-Aligned-Dashboard-Mockup.png" and `ui-ux-spec.md`, including:
    - Clear typography (Helvetica Neue).
    - Appropriate use of Mailchimp colors (e.g., Peppercorn for text, potential subtle background).
    - Visual distinction for sentiment (e.g., an icon or color-coded text: green for positive, red for negative, gray for neutral, as per mockup).
    - Hover and focus states that enhance interactivity (e.g., subtle background change like `subtle-yellow-tint`, focus ring like `cavendish-yellow`).
    - A visual indicator for a "selected" state (e.g., a more prominent border in `cavendish-yellow`, as per mockup).
5. When a `TrendCard` is clicked, an `onSelectTrend(trendId: string)` callback (passed as a prop) is triggered with the ID of the clicked trend.
6. The list of `TrendCard`s within the `TrendFeedPanel` is sortable by at least one criterion (e.g., "recency" - most recent `identified_date` first, or "score" - highest score first). For this story, implement sorting by `identified_date` (most recent first) as a default.
7. The `TrendCard` components are keyboard accessible (focusable and selectable with Enter/Space).

## Tasks / Subtasks

- [ ] Task 1: Create `TrendCard` Component Structure (AC: #1, #2)
  - [ ] Create `frontend/components/ui/TrendCard.tsx` (or `layout/TrendCard.tsx`).
  - [ ] Define props: `trend: TrendListItem`, `onSelect: (trendId: string) => void`, `isSelected: boolean`.
  - [ ] Lay out HTML structure to display `trend.name` (e.g., `h3`), `trend.identified_date` (formatted), `trend.score`, and `trend.sentiment`.
- [ ] Task 2: Style `TrendCard` (AC: #4)
  - [ ] Apply Tailwind CSS classes to match `Final-Mailchimp-Aligned-Dashboard-Mockup.png`.
    - Base card styling (padding, border `border-border-grey`, rounded corners).
    - Typography (font-helvetica-neue, text sizes, text-peppercorn).
    - Sentiment display: Use Lucide icons (e.g., `TrendingUp` for positive, `TrendingDown` for negative, `Minus` for neutral) and appropriate text colors (e.g., green, red, gray).
    - Implement hover state (e.g., `hover:bg-subtle-yellow-tint`).
    - Implement focus state (e.g., `focus:ring-2 focus:ring-cavendish-yellow focus:outline-none`).
    - Implement selected state (e.g., conditional class for `border-2 border-cavendish-yellow` if `isSelected` is true).
- [ ] Task 3: Implement `TrendCard` Interactivity (AC: #5, #7)
  - [ ] Add `onClick={() => onSelect(trend.id)}` to the main card element.
  - [ ] Add `role="button"` and `tabIndex={0}` to the main card element.
  - [ ] Add `onKeyDown` handler to trigger `onSelect(trend.id)` if `event.key === 'Enter' || event.key === ' '`.
- [ ] Task 4: Integrate `TrendCard` into `TrendFeedPanel` (AC: #3)
  - [ ] In `TrendFeedPanel.tsx` (or `app/(dashboard)/page.tsx` where trend list is managed):
    - [ ] Import `TrendCard`.
    - [ ] When trend data is successfully fetched and available:
      - [ ] Map over the `trends` array.
      - [ ] For each `trend` object, render `<TrendCard key={trend.id} trend={trend} onSelect={handleTrendSelect} isSelected={selectedTrendId === trend.id} />`.
      - [ ] `handleTrendSelect` function will update the `selectedTrendId` state (managed by `SelectedTrendContext` likely, set up in later stories or page state for now).
- [ ] Task 5: Implement Default Sorting (AC: #6)
  - [ ] Before rendering, sort the `trends` array by `identified_date` in descending order (most recent first). This can be done where the trends data is fetched or managed.

        ```typescript
        // Example sorting
        // const sortedTrends = [...trends].sort((a, b) => new Date(b.identified_date).getTime() - new Date(a.identified_date).getTime());
        ```

- [ ] Task 6: Unit Tests for `TrendCard` (AC: #1, #2, #4, #5, #7)
  - [ ] Create `frontend/components/ui/__tests__/TrendCard.test.tsx`.
  - [ ] Test rendering with mock `trend` data.
  - [ ] Test `onSelect` callback is called on click and key press.
  - [ ] Test conditional styling for `isSelected`.
  - [ ] Include accessibility checks (`jest-axe`).

## Dev Technical Guidance

- **`TrendListItem` Type:** Ensure the `trend` prop for `TrendCard` matches the `TrendListItem` interface defined in `frontend/lib/types.ts` (which should align with the backend API response from `/api/v1/trends`).

        ```typescript
        // frontend/lib/types.ts (example structure)
        // export interface TrendListItem {
        //   id: string;
        //   name: string;
        //   identified_date: string; // ISO8601 date string
        //   score: number;
        //   sentiment: 'positive' | 'negative' | 'neutral' | string; // Be flexible for now
        //   category?: string | null;
        //   summary?: string | null;
        // }
        ```

- **Date Formatting:** Format `trend.identified_date` (e.g., `new Date(trend.identified_date).toLocaleDateString()`).

- **Sentiment Visualization:** Use a combination of a Lucide icon and color to represent sentiment, as shown in `Final-Mailchimp-Aligned-Dashboard-Mockup.png`.
- **`isSelected` State:** The logic for which trend is currently selected will likely be managed by a parent component or context (`SelectedTrendContext` to be introduced/utilized more formally later). For this story, ensure `TrendCard` can visually reflect this prop.
- **Accessibility:** Making the `div` act like a button (`role="button"`, `tabIndex`, keyboard handlers) is crucial for accessibility. Ensure focus indicators are clear.
- **`shadcn/ui` Base:** Consider if `TrendCard` should be based on `shadcn/ui Card` component. Initialize `shadcn/ui Card` (`pnpm dlx shadcn-ui@latest add card`) and then style its parts (`Card`, `CardHeader`, `CardTitle`, `CardContent`, `CardDescription`, `CardFooter`) with Tailwind. The mockup looks like a simple clickable div with content, so a styled `div` might be more direct than a full `shadcn/ui Card` if headers/footers aren't used. The visual reference in `Final-Mailchimp-Aligned-Dashboard-Mockup.png` for "AI in Email Marketing" card is the primary guide.

## Story Progress Notes

### Completion Notes List

{Any notes about implementation choices, difficulties, or follow-up needed}

### Change Log

- 2025-05-17 - Kayvan Sylvan - Initial draft
