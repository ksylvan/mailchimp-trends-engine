# Story 4.3: Trend Filtering (Basic)

## Status: Draft

## Story

- As a Frontend Developer Agent
- I want to implement basic filtering controls (by category, by sentiment) in the "Trend Feed Panel"
- so that users can narrow down the list of displayed trends to find those most relevant to their interests, with filter controls styled like Mailchimp's.

## Acceptance Criteria (ACs)

1. UI controls for filtering trends are added to the "Trend Feed Panel".
    - A dropdown (`shadcn/ui Select`) allows filtering by trend category.
    - A set of buttons or a toggle group (`shadcn/ui Toggle Group` or styled `Button`s) allows filtering by sentiment (e.g., "All", "Positive", "Neutral", "Negative").
2. Filter controls are styled to align with Mailchimp's form elements (referencing `ui-ux-spec.md`, `Final-Mailchimp-Aligned-Dashboard-Mockup.png`).
3. The list of available categories for the category filter dropdown is populated dynamically (e.g., derived from the fetched trend data or a separate API endpoint if available; for MVP, can be based on unique categories present in the current trend list).
4. When a filter value is changed (category selected, sentiment button clicked), the list of displayed trends in the `TrendFeedPanel` updates reactively without a full page reload.
5. The backend API call to `/api/v1/trends` is updated to include selected filter parameters (e.g., `?category=Tech&sentiment=positive`).
6. The current active filter state is managed (e.g., via React Context - `TrendsDataContext` as proposed in `frontend-architecture.md` - or local state in the dashboard page/panel).
7. Filter controls are keyboard accessible and usable.

## Tasks / Subtasks

- [ ] Task 1: Create `TrendFilterControls` Component (AC: #1, #2, #7)
  - [ ] Create `frontend/features/trend-filtering/TrendFilterControls.tsx` (or within `components/layout/` if simpler for MVP).
  - [ ] Define props:
    - `activeFilters: { category: string | null, sentiment: string | null }`
    - `onFilterChange: (filterName: string, value: string | null) => void`
    - `categories: string[]` (for category dropdown options)
    - `sentiments: string[]` (e.g., ["All", "Positive", "Neutral", "Negative"])
  - [ ] Implement Category Filter:
    - [ ] Use `shadcn/ui Select` component.
    - [ ] Populate options from the `categories` prop. Include an "All Categories" option.
    - [ ] Its value should reflect `activeFilters.category`.
    - [ ] On change, call `onFilterChange('category', selectedValue)`.
  - [ ] Implement Sentiment Filter:
    - [ ] Use `shadcn/ui Toggle Group` or a series of styled `Button`s.
    - [ ] Options: "All", "Positive", "Neutral", "Negative".
    - [ ] The active sentiment should be visually indicated.
    - [ ] On click/toggle, call `onFilterChange('sentiment', selectedValue)`. ("All" would pass `null`).
  - [ ] Style controls using Tailwind to match Mailchimp aesthetics (clean, clear, good hit areas). Refer to mockup for "Category" and "Sentiment" filter appearance.
- [ ] Task 2: Manage Filter State (AC: #6)
  - [ ] In `frontend/contexts/TrendsDataContext.tsx` (or the component managing trend data, e.g., `app/(dashboard)/page.tsx`):
    - [ ] Add `filters: { category: string | null, sentiment: string | null }` to the context state.
    - [ ] Implement `updateFilters(newFilters: Partial<TrendFilters>)` function in the context that updates this state.
    - [ ] When `filters` state changes, trigger a re-fetch of trends (see Task 4).
- [ ] Task 3: Populate Filter Options (AC: #3)
  - [ ] In the component managing trend data:
    - [ ] After fetching trends, derive a unique list of categories present in the data: `const uniqueCategories = [...new Set(trends.map(t => t.category).filter(Boolean))];`.
    - [ ] Pass this `uniqueCategories` list to `TrendFilterControls`.
    - [ ] The sentiment options can be a static list: `["All", "Positive", "Neutral", "Negative"]`.
- [ ] Task 4: Update API Call with Filters (AC: #4, #5)
  - [ ] Modify the `getTrends` function in `frontend/lib/apiClient.ts` to accept a `filters` object.

        ```typescript
        // apiClient.ts
        // export const getTrends = async (filters?: { category?: string | null, sentiment?: string | null, /* other params */ }): Promise<{ trends: TrendListItem[], total_count: number }> => {
        //   const queryParams = new URLSearchParams();
        //   if (filters?.category) queryParams.append('category', filters.category);
        //   if (filters?.sentiment) queryParams.append('sentiment', filters.sentiment);
        //   // ...
        //   return WorkspaceApi(...);
        // };
        ```

  - [ ] In `TrendsDataContext` (or wherever `getTrends` is called):
    - [ ] When `filters` state changes (or on initial load with default filters), call `apiClient.getTrends(currentFilters)`.
    - [ ] Update the displayed trend list with the new results. Handle loading/error states.
- [ ] Task 5: Integrate `TrendFilterControls` into `TrendFeedPanel`
  - [ ] In `TrendFeedPanel.tsx`:
    - [ ] Import and render `TrendFilterControls`.
    - [ ] Pass the current `activeFilters` from context/state.
    - [ ] Pass the `updateFilters` function from context/state as `onFilterChange`.
    - [ ] Pass the derived `categories` and static `sentiments` lists.
- [ ] Task 6: Unit Tests for `TrendFilterControls` and Filter Logic
  - [ ] Test `TrendFilterControls` component:
    - [ ] Renders dropdowns/buttons correctly with given options.
    - [ ] `onFilterChange` is called with correct parameters when selections are made.
  - [ ] Test filter state management logic (e.g., in `TrendsDataContext` if applicable):
    - [ ] Verify `updateFilters` correctly changes state.
    - [ ] Verify API call is re-triggered with new filter parameters.

## Dev Technical Guidance

- **`shadcn/ui` Components:**
  - `Select`: Use for the category filter. Refer to `shadcn/ui` docs for `Select`, `SelectTrigger`, `SelectContent`, `SelectItem`, etc.
  - `Toggle Group`: Suitable for the sentiment filter where one option (or "All") is active. Alternatively, a group of `Button` components with custom state logic to manage selection. The mockup shows distinct buttons for "All", "Positive", "Neutral", "Negative".
- **State Management for Filters:** Using a React Context (`TrendsDataContext`) that holds both the trend list and the active filters is a clean way to manage this, as filter changes need to trigger re-fetching of the trend list.
- **"All" Option:** For filters like category or sentiment, an "All" option should effectively mean that filter parameter is not sent to the backend (or sent as `null`/empty).
- **API Parameters:** Ensure the backend API for `/api/v1/trends` (Story in Epic 3) is designed to accept `category` and `sentiment` query parameters.
- **Styling:** Filters in `Final-Mailchimp-Aligned-Dashboard-Mockup.png` are clean and simple. Category is a dropdown. Sentiment options are like segmented buttons. Emulate this.
- **Debouncing/Throttling:** Not strictly necessary for select dropdowns or button clicks, as these are discrete user actions. If a text-based filter were added later, debouncing would be important.

## Story Progress Notes

### Completion Notes List

{Any notes about implementation choices, difficulties, or follow-up needed}

### Change Log

2025-05-17 - Kayvan Sylvan - Initial draft
