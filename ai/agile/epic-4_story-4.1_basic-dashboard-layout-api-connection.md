# Story 4.1: Basic Dashboard Layout & API Connection

## Status: Draft

## Story

- As a Frontend Developer Agent
- I want to create the basic Next.js page structure for the main dashboard, implement its three-panel layout using Tailwind CSS, and establish an initial API connection to the backend's `/api/v1/trends` endpoint
- so that the foundational UI for displaying trends is in place and can fetch initial trend data.

## Acceptance Criteria (ACs)

1. A Next.js page (e.g., `app/(dashboard)/page.tsx` and its corresponding `layout.tsx`) is created to serve as the main dashboard view.
2. The layout (`app/(dashboard)/layout.tsx`) implements the three-column panel structure (Trend Feed, Trend Details, AI Content) as per `ui-ux-spec.md` and `Final-Mailchimp-Aligned-Dashboard-Mockup.png`, styled with Tailwind CSS.
3. Placeholder components or simple `div`s are used for the three main panels initially.
4. The main dashboard page (`app/(dashboard)/page.tsx`) attempts to fetch a list of trends from the backend API (`/api/v1/trends`) on initial load using the `apiClient.ts` service.
5. The fetched trend names (or placeholder data if API is not fully ready) are displayed in the "Trend Feed" panel area.
6. Basic loading and error states for the API call are handled and visually indicated in the UI (e.g., "Loading trends..." message, "Failed to load trends." message).
7. The dashboard layout is responsive, hinting at the single-column stack for smaller screens (full responsiveness handled in later stories but basic structure should allow it).
8. The global header component (from `frontend-architecture.md` foundational components, if created separately, or implemented here) is included in the root layout (`app/layout.tsx` or `app/(dashboard)/layout.tsx`).

## Tasks / Subtasks

- [ ] Task 1: Implement Root and Dashboard Layouts (AC: #1, #2, #8)
  - [ ] If not already present, ensure `frontend/app/layout.tsx` (root layout) includes global providers (e.g., for Context API planned later) and potentially the `GlobalHeader`.
  - [ ] Create `frontend/app/(dashboard)/layout.tsx`.
    - [ ] Implement the three-column flexbox or grid structure using Tailwind CSS classes to define the "Trend Feed & Filters Panel" (left), "Trend Details & Visualization Panel" (center), and "AI Content Generation Panel" (right). Refer to `frontend-architecture.md` for panel component names and `Final-Mailchimp-Aligned-Dashboard-Mockup.png`.
    - [ ] Ensure the layout is contained within a main content area below the `GlobalHeader`.
  - [ ] Create `frontend/app/(dashboard)/page.tsx`.
- [ ] Task 2: Implement Placeholder Panels (AC: #3)
  - [ ] In `app/(dashboard)/page.tsx`, or by creating basic panel components (e.g., `TrendFeedPanel.tsx`, `TrendDetailsPanel.tsx`, `AiContentPanel.tsx` in `components/layout/` as per `frontend-architecture.md`):
    - [ ] Render simple `div`s or placeholder components with titles for each of the three panels within the three-column layout.
    - [ ] Style them minimally to delineate the areas.
- [ ] Task 3: Implement API Call for Trends (AC: #4, #5, #6)
  - [ ] In `app/(dashboard)/page.tsx` (if a Server Component fetching initial data) or in the `TrendFeedPanel` component (if client-side fetching is preferred for dynamic updates):
    - [ ] Use `useEffect` (for client component) or direct `await` (for server component) to call `apiClient.getTrends()`.
    - [ ] Store fetched trends, loading state, and error state (e.g., using `useState`).
    - [ ] Display a "Loading trends..." message while fetching.
    - [ ] If an error occurs, display an error message (e.g., "Failed to fetch trends.").
    - [ ] If successful, map over the `trends` array and display `trend.name` in the "Trend Feed" panel area.
- [ ] Task 4: Basic Responsiveness Hint (AC: #7)
  - [ ] Ensure the Tailwind classes used for the three-column layout have basic responsive modifiers that would allow them to stack vertically on smaller screens (e.g., `flex flex-col lg:flex-row`). Detailed responsive styling will be refined later.
- [ ] Task 5: Integrate `apiClient.ts` (AC: #4)
  - [ ] Ensure `frontend/lib/apiClient.ts` is created (if not already from backend connectivity tests in Epic 1) and exports a `getTrends` function that calls the backend `/api/v1/trends` endpoint.
  - [ ] Ensure `NEXT_PUBLIC_API_URL` is correctly configured in `.env.local` for development.

## Dev Technical Guidance

- **Layout Implementation:** Use Tailwind CSS's Flexbox or CSS Grid utilities for the three-column layout. Refer to `frontend-architecture.md` for panel component structure and `Final-Mailchimp-Aligned-Dashboard-Mockup.png` for visual proportions.
- **Panel Components:** It's recommended to create separate components for each panel (`TrendFeedPanel`, `TrendDetailsPanel`, `AiContentPanel`) as outlined in `frontend-architecture.md` and `ui-ux-spec.md`. For this story, these can be simple skeletons.
- **Data Fetching:**
  - **Server Component Approach (Recommended for initial load):** Make `app/(dashboard)/page.tsx` an `async` component.

      ```typescript
      // app/(dashboard)/page.tsx
      import { apiClient } from '@/lib/apiClient'; // Assuming apiClient is structured for RSC
      // ... other imports
      async function getTrendsData() {
          try { return await apiClient.getTrends(); } catch (e) { return null; /* handle error appropriately */ }
      }
      export default async function DashboardPage() {
          const initialTrendsData = await getTrendsData();
          // Pass initialTrendsData to client components for TrendFeedPanel etc.
          return ( /* JSX with panels */ );
      }
      ```

  - **Client Component Approach (If preferred for this part, or for dynamic updates within TrendFeedPanel):** Use `useEffect` and `useState` within the component that displays the trends.
- **API Endpoint:** The backend `/api/v1/trends` endpoint is expected to be implemented by the time this story is worked on (or at least its schema defined, allowing frontend to mock responses). For this story, the frontend should attempt the call; handling mock data if the backend isn't fully ready is acceptable for initial UI work.
- **Styling:** Apply basic background colors and typography from the Mailchimp theme (defined in `tailwind.config.js` and `globals.css`) to the page and panels for initial visual alignment.
- **Error Handling:** Simple text messages for loading/error states are sufficient for this story. More sophisticated error display (e.g., Toasts) can come later.

## Story Progress Notes

### Completion Notes List

### Change Log

- 2025-05-17 - Kayvan Sylvan - Initial draft
