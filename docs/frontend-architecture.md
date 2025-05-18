# Mailchimp Marketing Trends Engine Frontend Architecture Document

## Table of Contents

- [Mailchimp Marketing Trends Engine Frontend Architecture Document](#mailchimp-marketing-trends-engine-frontend-architecture-document)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Overall Frontend Philosophy \& Patterns](#overall-frontend-philosophy--patterns)
  - [Detailed Frontend Directory Structure](#detailed-frontend-directory-structure)
    - [Notes on Frontend Structure](#notes-on-frontend-structure)
  - [Component Breakdown \& Implementation Details](#component-breakdown--implementation-details)
    - [Component Naming \& Organization](#component-naming--organization)
    - [Template for Component Specification](#template-for-component-specification)
      - [Component: `{ComponentName}`](#component-componentname)
    - [Foundational Components](#foundational-components)
      - [Component: `GlobalHeader`](#component-globalheader)
      - [Component: `TrendFeedPanel`](#component-trendfeedpanel)
      - [Component: `TrendCard`](#component-trendcard)
      - [Component: `TrendDetailsPanel`](#component-trenddetailspanel)
      - [Component: `AiContentPanel`](#component-aicontentpanel)
  - [State Management In-Depth](#state-management-in-depth)
    - [Chosen Solution \& Decision Guide](#chosen-solution--decision-guide)
    - [Context API Usage](#context-api-usage)
      - [1. `TrendsDataContext`](#1-trendsdatacontext)
      - [2. `SelectedTrendContext`](#2-selectedtrendcontext)
    - [Potential Lightweight Global State Manager (if deemed necessary)](#potential-lightweight-global-state-manager-if-deemed-necessary)
  - [API Interaction Layer](#api-interaction-layer)
    - [Client/Service Structure](#clientservice-structure)
    - [Data Fetching Strategy](#data-fetching-strategy)
    - [Error Handling \& Retries (Frontend)](#error-handling--retries-frontend)
  - [Routing Strategy](#routing-strategy)
    - [Route Definitions](#route-definitions)
    - [Route Guards / Protection](#route-guards--protection)
  - [Styling Conventions](#styling-conventions)
    - [Tailwind CSS Configuration \& Usage](#tailwind-css-configuration--usage)
    - [Mailchimp Design Harmony](#mailchimp-design-harmony)
  - [Forms and User Input Handling](#forms-and-user-input-handling)
    - [Form Management](#form-management)
    - [Validation](#validation)
    - [Submission](#submission)
  - [Frontend Testing Strategy](#frontend-testing-strategy)
    - [Component Testing](#component-testing)
    - [UI Integration/Flow Testing](#ui-integrationflow-testing)
    - [End-to-End UI Testing Tools \& Scope](#end-to-end-ui-testing-tools--scope)
    - [Mocking API Calls](#mocking-api-calls)
  - [Accessibility (AX) Implementation Details](#accessibility-ax-implementation-details)
  - [Performance Considerations](#performance-considerations)
  - [Internationalization (i18n) and Localization (l10n) Strategy](#internationalization-i18n-and-localization-l10n-strategy)
  - [Feature Flag Management](#feature-flag-management)
  - [Frontend Security Considerations](#frontend-security-considerations)
  - [Browser Support and Progressive Enhancement](#browser-support-and-progressive-enhancement)
  - [Frontend Architecture Document Review Checklist Summary](#frontend-architecture-document-review-checklist-summary)

## Introduction

This document details the technical architecture specifically for the frontend of the Mailchimp Marketing Trends Engine (MVP). It complements the main Mailchimp Marketing Trends Engine (MVP) Architecture Document and the UI/UX Specification. This document details the frontend architecture and **builds upon the foundational decisions** (e.g., overall tech stack, CI/CD, primary testing tools) defined in the main Mailchimp Marketing Trends Engine (MVP) Architecture Document (`docs/architecture.md`). **Frontend-specific elaborations or deviations from general patterns must be explicitly noted here.** The goal is to provide a clear blueprint for frontend development, ensuring consistency, maintainability, and alignment with the overall system design and user experience goals.

- **Link to Main Architecture Document:** [`docs/architecture.md`][architecture-doc]
- **Link to UI/UX Specification:** [`docs/ui-ux-spec.md`][ui-ux-spec]
- **Primary Design Mockup** [`docs/Final-Mailchimp-Aligned-Dashboard-Mockup.png`][mock-up-image]
- **Link to Mailchimp User Guide (for UI/UX Inspiration):** [`docs/515-Media-Mailchimp-User-Guide-REV2.pdf`][Media-Kit-Mailchimp]

## Overall Frontend Philosophy & Patterns

The frontend architecture for the Mailchimp Marketing Trends Engine MVP is designed for rapid development, maintainability, and a user experience that aligns closely with Mailchimp's established design language. It leverages a modern, type-safe technology stack and adheres to best practices for building responsive and accessible single-page applications.

- **Framework & Core Libraries:**
  - **Next.js `~15.3.2` with React `~18.x.x` (inferred from Next.js version):** The core framework for building the Single-Page Application (SPA). We will utilize the **App Router** for routing, layouts, and server components where appropriate.
  - **TypeScript `~5.5.2`:** For type safety and improved developer experience.
        These are derived from the 'Definitive Tech Stack Selections' in the main Architecture Document.
- **Component Architecture:**
  - The architecture will follow a **feature-based organization** for components where components specific to a feature are co-located.
  - **Globally reusable UI components** (e.g., buttons, cards, inputs if not directly used from `shadcn/ui` as is) will be in a shared directory.
  - **`shadcn/ui`** will serve as the foundation for unstyled, accessible components. These components will be added to the project via its CLI and customized as needed.
  - We will adopt a **Presentational and Container Component** pattern where applicable, separating concerns:
    - **Presentational Components:** Focus on the UI (how things look). Receive data and callbacks exclusively via props. Often pure functions.
    - **Container Components:** Focus on how things work. May contain state, logic, and data fetching, passing data down to presentational components.
- **State Management Strategy:**
  - **React Context API / Hooks:** Preferred for MVP for managing local and moderately shared state due to simplicity. This is referenced from the main Architecture Document and detailed further in the "State Management In-Depth" section.
  - A lightweight global state manager (e.g., Zustand or Jotai) will only be considered if specific complex global state scenarios arise that are cumbersome to manage with Context API alone. Redux is explicitly avoided for MVP.
- **Data Flow:**
  - Primarily **unidirectional data flow**, characteristic of React applications.
  - Data fetching from the backend API will be managed within Server Components where appropriate for initial data load, or within Client Components using React Hooks (e.g., `useEffect` with `Workspace`) for dynamic data fetching, mutations, and client-side interactions.
  - For client-side data fetching that requires caching, optimistic updates, or revalidation, SWR or TanStack Query (React Query) might be considered if a compelling need arises beyond simple `Workspace`/`useEffect`. However, for MVP, direct `Workspace` calls are the default.
- **Styling Approach:**
  - **Tailwind CSS `~3.5.1`:** The primary styling solution, following a utility-first approach.
  - **`shadcn/ui` components** will be styled using Tailwind CSS utility classes, often by customizing the versions brought in by the `shadcn/ui` CLI.
  - **Configuration File(s):** `frontend/tailwind.config.js`, `frontend/postcss.config.js` (if further PostCSS plugins are needed beyond what Next.js provides for Tailwind), `frontend/styles/globals.css` (for base styles, Tailwind directives, and global CSS variables).
  - **Key conventions:**
    - Utility-first for most styling.
    - Custom, reusable component styles will be achieved by creating new React components that encapsulate specific combinations of Tailwind utilities or `shadcn/ui` components with custom styling.
    - Theme extensions (colors, fonts, spacing to align with Mailchimp) will be defined in `tailwind.config.js` under `theme.extend`. The Mailchimp color palette and typography from `ui-ux-spec.md` will be integrated here.
    - Adherence to Mailchimp's visual style as per `515-Media-Mailchimp-User-Guide-REV2.pdf` and `Final-Mailchimp-Aligned-Dashboard-Mockup.png` is paramount.
- **Key Design Patterns Used:**
  - **Hooks:** For stateful logic and side effects in functional components.
  - **Provider Pattern:** For managing global/shared state with React Context.
  - **Container/Presentational Components:** To separate concerns and improve reusability.
  - **Service Pattern (for API calls):** API interaction logic will be encapsulated in dedicated service modules/functions.
  - **Modular Design:** Code will be organized into modules with clear responsibilities (features, components, services, hooks, etc.).

This philosophy aims for a balance between rapid development for the MVP and a solid foundation for future iterations.

Next, I will define the "Detailed Frontend Directory Structure."

## Detailed Frontend Directory Structure

The frontend application, managed with `pnpm` and residing in the `/frontend` directory of the monorepo, will follow a structure that aligns with Next.js App Router conventions and promotes modularity and scalability.

```plaintext
frontend/
├── app/                                # Next.js App Router: Core routing, layouts, and page components.
│   │                                   # MUST contain route segments, layouts, and page components.
│   ├── (dashboard)/                    # Route group for the main dashboard interface.
│   │   │                               # Conceptually represents the SPA's main view.
│   │   ├── layout.tsx                  # Layout specific to the dashboard (e.g., 3-panel structure).
│   │   │                               # MUST define the primary three-column panel structure.
│   │   └── page.tsx                    # Entry page component for the dashboard.
│   │                                   # MUST orchestrate the main panels.
│   ├── api/                            # Next.js Route Handlers (if any frontend-specific backend logic is needed, e.g., BFF patterns).
│   │   │                               # For MVP, primary API is external (FastAPI backend); use sparingly.
│   │   └── (example)/
│   │       └── route.ts
│   ├── favicon.ico                     # Application favicon.
│   │                                   # MUST be present.
│   ├── globals.css                     # Global styles, Tailwind CSS base directives, and Mailchimp theme variables.
│   │                                   # MUST contain base styles, CSS variable definitions for Mailchimp theme, Tailwind base/components/utilities.
│   └── layout.tsx                      # Root layout for the entire application.
│                                       # MUST include global providers (e.g., ThemeProvider, State Management Contexts).
├── components/                         # Shared/Reusable UI Components.
│   ├── ui/                             # Base UI elements from shadcn/ui or custom-built generics.
│   │   │                               # MUST contain only generic, reusable, presentational UI elements, often mapped from shadcn/ui. MUST NOT contain business logic.
│   │   ├── button.tsx                  # shadcn/ui button (or custom wrapper if needed).
│   │   ├── card.tsx                    # shadcn/ui card.
│   │   ├── input.tsx                   # shadcn/ui input.
│   │   ├── select.tsx                  # shadcn/ui select.
│   │   ├── chart.tsx                   # Wrapper for chart.js or other charting library.
│   │   └── ...                         # Other shadcn/ui components added via CLI.
│   └── layout/                         # Layout-specific components (e.g., panel wrappers if more complex).
│       │                               # MUST contain components structuring specific parts of page layouts, not page content itself.
│       ├── TrendFeedPanel.tsx          # Component for the "Trend Feed & Filters" panel.
│       ├── TrendDetailsPanel.tsx       # Component for the "Trend Details & Visualization" panel.
│       └── AiContentPanel.tsx          # Component for the "AI Content Generation" panel.
├── features/                           # Feature-specific UI components, hooks, and logic (if complex enough to warrant separation).
│   │                                   # For MVP, most panel-specific components might live in `components/layout/` or directly in `app/(dashboard)/page.tsx`.
│   │                                   # This is a placeholder for future expansion if features become more distinct.
│   └── trend-filtering/
│       ├── TrendFilterControls.tsx     # Component for filter controls (dropdowns, toggles).
│       └── useTrendFilters.ts          # Custom hook for managing filter state and logic.
├── contexts/                           # React Context API providers and consumers for shared state.
│   │                                   # MUST be used for localized state not suitable for prop drilling but not needed globally via Zustand/Jotai.
│   └── TrendContext.tsx                # Example: Context for selected trend, shared between panels.
├── hooks/                              # Global/sharable custom React Hooks.
│   │                                   # MUST be generic and usable by multiple features/components.
│   └── useCopyToClipboard.ts           # Example: Hook for copy-to-clipboard functionality.
├── lib/                                # Utility functions, helpers, constants, API client configuration.
│   │                                   # MUST contain pure functions, constants, and API service definitions.
│   ├── apiClient.ts                    # Axios or Workspace client setup for backend API.
│   ├── utils.ts                        # General utility functions (formatting, etc.).
│   ├── constants.ts                    # Application-wide constants.
│   └── types.ts                        # Shared TypeScript type definitions and interfaces for frontend.
├── public/                             # Static assets (images, fonts not handled by Next/font, etc.).
│   └── images/
│       └── mailchimp-logo.svg
├── styles/                             # Contains `globals.css`. Further CSS files if not using Tailwind exclusively or for specific overrides.
├── .env.local.example                  # Example environment variables for frontend (e.g., NEXT_PUBLIC_API_URL).
├── Dockerfile                          # Docker build instructions for frontend.
├── next.config.mjs                     # Next.js configuration file.
├── package.json                        # Frontend dependencies and scripts (pnpm).
├── pnpm-lock.yaml                      # pnpm lock file.
├── postcss.config.mjs                  # PostCSS configuration (primarily for Tailwind CSS).
├── tailwind.config.js                  # Tailwind CSS configuration (theme, plugins).
└── tsconfig.json                       # TypeScript configuration for frontend.
```

### Notes on Frontend Structure

- **App Router (`app/`):** This is the primary location for defining routes, layouts, and pages as per Next.js 13+ conventions.
- **Route Groups (`(dashboard)`):** Used to organize routes without affecting the URL path. The main dashboard is grouped for clarity.
- **Components (`components/`):**
  - `components/ui/`: For `shadcn/ui` components and other generic, highly reusable UI primitives. These are generally presentational.
  - `components/layout/`: For major structural components of the dashboard panels. These might be container-like, fetching their own data or receiving it from the main page.
- **Features (`features/`):** This directory is for more complex, self-contained features that might emerge. For the MVP's three-panel design, panel-specific logic might initially reside within the panel components themselves or be orchestrated by `app/(dashboard)/page.tsx`. If a panel's logic (e.g., filtering) becomes very complex, it could be extracted into this directory.
- **Contexts (`contexts/`):** To house React Context for state shared between sibling components (like the panels) that isn't global enough for a dedicated state manager but too complex for simple prop drilling.
- **Hooks (`hooks/`):** For reusable stateful logic.
- **Lib (`lib/`):** A general-purpose directory for utilities, API client setup, type definitions, and constants.
  - `lib/apiClient.ts`: Centralized setup for `Workspace` or Axios to interact with the `/api/v1` backend. Will include base URL configuration, and could include interceptors for request/response handling if needed.
  - `lib/types.ts`: Contains shared TypeScript interfaces and types used across the frontend (e.g., API response shapes, data models used by components).
- **Mailchimp Alignment:** The structure supports creating a Mailchimp-aligned UI by centralizing theme configurations in `tailwind.config.js` and `globals.css`, and using `shadcn/ui` as a base for components that can be styled to match Mailchimp's aesthetics.

This structure should provide a clear and maintainable organization for the Mailchimp Marketing Trends Engine frontend.

Next, I will move to "Component Breakdown & Implementation Details," starting with naming/organization and the template, then outlining some foundational components based on the `ui-ux-spec.md`.

## Component Breakdown & Implementation Details

This section outlines the conventions for UI components and provides specifications for foundational components derived from the `ui-ux-spec.md` and `Final-Mailchimp-Aligned-Dashboard-Mockup.png`.

### Component Naming & Organization

- **Component Naming Convention:** `PascalCase` for files and component names (e.g., `TrendCard.tsx`, `FilterDropdown.tsx`). All component files MUST follow this convention.
- **Organization:**
  - **Generic UI Primitives:** Located in `frontend/components/ui/`. These are typically `shadcn/ui` components added via CLI (e.g., `button.tsx`, `card.tsx`, `select.tsx`) or custom wrappers around them if specific default styling or behavior is needed project-wide.
  - **Layout Components:** Major structural UI parts like the panels themselves will be in `frontend/components/layout/` (e.g., `TrendFeedPanel.tsx`, `TrendDetailsPanel.tsx`, `AiContentPanel.tsx`).
  - **Feature-Specific Components:** Components used exclusively within a distinct feature (e.g., complex filter controls for the trend feed) may reside in `frontend/features/[feature-name]/components/` or, for simpler cases in MVP, be co-located with the panel component that uses them.
  - **Page-Level Components:** The main page orchestrating the panels is `frontend/app/(dashboard)/page.tsx`.

### Template for Component Specification

For each significant UI component identified, the following details MUST be provided. This template will guide the implementation.

#### Component: `{ComponentName}`

- **Purpose:** {Briefly describe what this component does and its role in the UI. MUST be clear and concise.}
- **Source File(s):** {e.g., `frontend/components/ui/ComponentName.tsx`. MUST be the exact path.}
- **Visual Reference:** {Link to specific section in `Final-Mailchimp-Aligned-Dashboard-Mockup.png` or description in `ui-ux-spec.md`.}
- **Props (Properties):**

    | Prop Name | Type                                      | Required? | Default Value | Description                                                                                               |
    | :-------------- | :---------------------------------------- | :-------- | :------------ | :--------------------------------------------------------------------------------------------------------- |
    | `{propName}` | `{Specific primitive, imported type, or inline interface/type definition}` | {Yes/No}  | {If any}    | {MUST clearly state the prop's purpose and any constraints, e.g., 'Must be a positive integer.'}         |

- **Internal State (if any):**

    | State Variable | Type      | Initial Value | Description                                                                    |
    | :-------------- | :-------- | :------------ | :----------------------------------------------------------------------------- |
    | `{stateVar}` | `{type}`  | `{value}`     | {Description of state variable and its purpose.}                               |

- **Key UI Elements / Structure:**

    ```html
    <header class="bg-peppercorn text-white p-4 flex items-center">
    <!-- HTML.css.javascript snippets shown here -->
    </header>
    ```

- **Events Handled / Emitted:**
  - **Handles:** {e.g., `onClick` on a button.}
  - **Emits (Callbacks):** {e.g., `onSelect: (value: string) => void`. Describe props that are functions.}
- **Actions Triggered (Side Effects):**
  - **State Management:** {e.g., "Calls `setSelectedTrend(trend)` from `TrendContext`."}
  - **API Calls:** {Specify which service/function from `lib/apiClient.ts` or feature-specific service is called. e.g., "Calls `apiClient.getTrendDetails(trendId)`."}
- **Styling Notes:**
  - {MUST reference specific `shadcn/ui` components used as a base and key Tailwind CSS classes for customization. Refer to `ui-ux-spec.md` for Mailchimp color palette (Cavendish Yellow, Peppercorn, etc.) and typography (Helvetica Neue) to be applied via `tailwind.config.js` and utility classes.}
- **Accessibility Notes:**
  - {MUST list specific ARIA attributes (e.g., `aria-label`), keyboard navigation patterns, and focus management requirements, aiming for WCAG 2.1 AA.}

-----

### Foundational Components

Based on the `ui-ux-spec.md` and the three-panel dashboard design, here are some foundational components:

#### Component: `GlobalHeader`

- **Purpose:** Displays the Mailchimp-styled global header for brand consistency and context.
- **Source File(s):** `frontend/components/layout/GlobalHeader.tsx`
- **Visual Reference:** `ui-ux-spec.md` (Global Header description), `Final-Mailchimp-Aligned-Dashboard-Mockup.png` (top bar).
- **Props (Properties):** None anticipated for MVP (static content).
- **Internal State (if any):** None.
- **Key UI Elements / Structure:**

    ```html
    <header class="bg-peppercorn text-white p-4 flex items-center">
      {/* Mailchimp Logo (e.g., an SVG or img tag) */}
      <img src="/images/mailchimp-logo.svg" alt="Mailchimp" class="h-8 mr-4" />
      <h1 class="text-xl font-helvetica-neue">Marketing Trends</h1>
      {/* Placeholder for potential user/account info on the right, as seen in mockups */}
    </header>
    ```

- **Events Handled / Emitted:** None.
- **Actions Triggered (Side Effects):** None.
- **Styling Notes:**
  - Uses Mailchimp colors (`peppercorn` for background, `white` for text) and `Helvetica Neue` font as defined in `tailwind.config.js`.
  - Spacing and logo treatment as per `Final-Mailchimp-Aligned-Dashboard-Mockup.png`.
- **Accessibility Notes:**
  - `<header>` landmark.
  - Logo image MUST have appropriate `alt` text.
  - Heading (`<h1>`) provides page context.

#### Component: `TrendFeedPanel`

- **Purpose:** Displays the list of marketing trends and provides filtering controls. This corresponds to the "Trend Feed & Filters Panel" in the UI/UX spec.
- **Source File(s):** `frontend/components/layout/TrendFeedPanel.tsx`
- **Visual Reference:** `ui-ux-spec.md` (Trend Feed & Filters Panel description, User Flow 1), `Final-Mailchimp-Aligned-Dashboard-Mockup.png` (left column).
- **Props (Properties):**

    | Prop Name | Type                                      | Required? | Default Value | Description                                                                                               |
    | :-------------- | :---------------------------------------- | :-------- | :------------ | :--------------------------------------------------------------------------------------------------------- |
    | `trends`        | `Array<TrendListItem>` (`lib/types.ts`)  | Yes       | N/A           | Array of trend data to display.                                                                              |
    | `isLoading`     | `boolean`                                 | Yes       | N/A           | Indicates if trend data is currently loading.                                                               |
    | `error`         | `string | null`                          | Yes       | N/A           | Error message if trend data fetching failed.                                                              |
    | `onSelectTrend` | `(trendId: string) => void`             | Yes       | N/A           | Callback when a user selects a trend.                                                                      |
    | `activeFilters` | `TrendFilters` (`lib/types.ts`)           | Yes       | N/A           | Current active filter values.                                                                              |
    | `onFilterChange`| `(newFilters: TrendFilters) => void`    | Yes       | N/A           | Callback when filter values change.                                                                        |
    | `categories`    | `Array<string>`                           | Yes       | `[]`          | List of available categories for the filter dropdown.                                                    |

- **Internal State (if any):** Minimal; primarily driven by props. Could have local UI state for filter dropdown open/close if not handled by `shadcn/ui` select.
- **Key UI Elements / Structure:**

    ```html
    <aside class="bg-white p-6 shadow-md rounded-lg flex flex-col space-y-4 h-full">
      <h2 class="text-lg font-bold font-helvetica-neue text-peppercorn">Current Trends</h2>
      {/* TrendFilterControls component will be used here, passing activeFilters, onFilterChange, categories */}
      <div class="flex-grow overflow-y-auto space-y-3">
        {/* if isLoading, show shimmer/spinner */}
        {/* if error, show error message */}
        {/* if !isLoading && !error && trends.length === 0, show "No trends found" message */}
        {/* trends.map(trend => <TrendCard key={trend.id} trend={trend} onSelect={onSelectTrend} />) */}
      </div>
    </aside>
    ```

- **Events Handled / Emitted:**
  - Handles: Interactions with `TrendFilterControls`, clicks on `TrendCard` items.
  - Emits: `onSelectTrend`, `onFilterChange` via props.
- **Actions Triggered (Side Effects):** None directly; orchestrates child components.
- **Styling Notes:**
  - Panel styling (`bg-white`, `shadow-md`, `rounded-lg`, padding) as per mockup.
  - Typography (`Helvetica Neue`, `Peppercorn` color for title) as per Mailchimp style.
  - Scrollable trend list.
- **Accessibility Notes:**
  - `<aside>` landmark.
  - `<h2>` for panel title.
  - Loading states MUST be announced to screen readers (e.g., `aria-live`).
  - Ensure filter controls within `TrendFilterControls` are fully accessible.
  - Ensure `TrendCard` items are keyboard focusable and selectable.

#### Component: `TrendCard`

- **Purpose:** Displays a single trend item in the Trend Feed Panel.
- **Source File(s):** `frontend/components/ui/TrendCard.tsx` (assuming it's a reusable UI element, styled for this project)
- **Visual Reference:** `ui-ux-spec.md` (Trend Card description within Trend Feed Panel), `Final-Mailchimp-Aligned-Dashboard-Mockup.png`.
- **Props (Properties):**

    | Prop Name | Type                                      | Required? | Default Value | Description                                                                                               |
    | :-------------- | :---------------------------------------- | :-------- | :------------ | :--------------------------------------------------------------------------------------------------------- |
    | `trend`         | `TrendListItem` (`lib/types.ts`)         | Yes       | N/A           | The trend data to display.                                                                                   |
    | `onSelect`      | `(trendId: string) => void`             | Yes       | N/A           | Callback function when the card is clicked.                                                                |
    | `isSelected`    | `boolean`                                 | No        | `false`       | Whether the card is currently selected.                                                                    |

- **Internal State (if any):** None.
- **Key UI Elements / Structure:**

    ```html
    <div class="border border-border-grey rounded-md p-4 cursor-pointer hover:bg-subtle-yellow-tint focus:outline-none focus:ring-2 focus:ring-cavendish-yellow"
         role="button" tabindex="0" onClick={() => onSelect(trend.id)} onKeyDown={(e) => e.key === 'Enter' && onSelect(trend.id)}>
      <h3 class="font-bold font-helvetica-neue text-peppercorn">{trend.name}</h3>
      <p class="text-sm text-gray-600 font-helvetica-neue">Date: {new Date(trend.identified_date).toLocaleDateString()}</p>
      <p class="text-sm text-gray-600 font-helvetica-neue">Score: {trend.score}</p>
      <p class="text-sm text-gray-600 font-helvetica-neue capitalize">Sentiment: {trend.sentiment}</p>
      {/* Visual indicator for selected state, e.g., yellow border - class applied conditionally based on isSelected prop */}
    </div>
    ```

- **Events Handled / Emitted:**
  - Handles: `onClick`, `onKeyDown` (for Enter key).
  - Emits: `onSelect` prop.
- **Actions Triggered (Side Effects):** Calls `onSelect` prop.
- **Styling Notes:**
  - Based on `shadcn/ui Card` or custom styled `div`.
  - Border (`border-border-grey`), padding, hover state (`bg-subtle-yellow-tint`), selected state (e.g., `border-cavendish-yellow border-2`) as per mockup/spec.
  - Typography and colors to align with Mailchimp style.
- **Accessibility Notes:**
  - `role="button"` and `tabindex="0"` to make it keyboard focusable and interactive.
  - Handles `Enter` key press for selection.
  - `aria-pressed={isSelected}` if it acts like a toggle, or `aria-current="true"` if it indicates current selection in a list.
  - Clear focus indicator.

#### Component: `TrendDetailsPanel`

- **Purpose:** Displays detailed information and a time-series visualization for a selected trend.
- **Source File(s):** `frontend/components/layout/TrendDetailsPanel.tsx`
- **Visual Reference:** `ui-ux-spec.md` (Trend Details & Visualization Panel), `Final-Mailchimp-Aligned-Dashboard-Mockup.png` (center column).
- **Props (Properties):**

    | Prop Name | Type                                      | Required? | Default Value | Description                                                                                               |
    | :-------------- | :---------------------------------------- | :-------- | :------------ | :--------------------------------------------------------------------------------------------------------- |
    | `selectedTrend` | `TrendDetailResponse | null`(`lib/types.ts`) | Yes       | N/A           | The detailed data of the selected trend, or null if no trend is selected.                               |
    | `isLoading`     | `boolean`                                 | Yes       | N/A           | Indicates if trend details are loading.                                                                    |
    | `error`         | `string | null`                          | Yes       | N/A           | Error message if fetching details failed.                                                                 |

- **Internal State (if any):** None. Chart component itself might have internal state.
- **Key UI Elements / Structure:**

    ```html
    <section class="bg-white p-6 shadow-md rounded-lg flex flex-col space-y-4 h-full">
      {/* if isLoading, show shimmer/spinner */}
      {/* if error, show error message */}
      {/* if !selectedTrend && !isLoading && !error, show "Select a trend to see details" message */}
      {/* if selectedTrend: */}
      <>
        <h2 class="text-xl font-bold font-helvetica-neue text-peppercorn">{selectedTrend.name}</h2>
        {/* Display key metrics: score, sentiment, category, summary, etc. */}
        <div class="flex-grow">
          {/* ChartWrapper component for TrendDataPointSchema history */}
          {/* <ChartComponent data={selectedTrend.history} /> */}
        </div>
      </>
    </section>
    ```

- **Events Handled / Emitted:** None directly.
- **Actions Triggered (Side Effects):** None directly.
- **Styling Notes:**
  - Panel styling as per mockup.
  - Chart styling (colors, axes) to align with Mailchimp aesthetics (Cavendish Yellow for primary data lines).
- **Accessibility Notes:**
  - `<section>` landmark with `aria-labelledby` pointing to the `<h2>` title.
  - Ensure chart has an accessible name (`aria-label`) and that key data points are also available textually (as suggested in UI/UX spec). WCAG 2.1 AA for chart contrast.

#### Component: `AiContentPanel`

- **Purpose:** Allows users to generate AI-powered marketing content ideas based on the selected trend.
- **Source File(s):** `frontend/components/layout/AiContentPanel.tsx`
- **Visual Reference:** `ui-ux-spec.md` (AI Content Generation Panel), `Final-Mailchimp-Aligned-Dashboard-Mockup.png` (right column).
- **Props (Properties):**

    | Prop Name | Type                                      | Required? | Default Value | Description                                                                                               |
    | :-------------- | :---------------------------------------- | :-------- | :------------ | :--------------------------------------------------------------------------------------------------------- |
    | `selectedTrendId`| `string | null`                         | Yes       | N/A           | The ID of the currently selected trend. Null if no trend selected.                                       |
    | `selectedTrendName`| `string | null`                       | Yes       | N/A           | The Name of the currently selected trend. Null if no trend selected.                                     |

- **Internal State (if any):**

    | State Variable | Type      | Initial Value | Description                                                                    |
    | :-------------- | :-------- | :------------ | :----------------------------------------------------------------------------- |
    | `generatedContent` | `GeneratedContentSchema | null`(`lib/types.ts`) | `null`        | Stores the AI-generated content.                                             |
    | `isLoading`     | `boolean` | `false`       | True when content generation is in progress.                                  |
    | `error`         | `string | null` | `null`        | Stores error message if generation fails.                                    |

- **Key UI Elements / Structure:**

    ```html
    <section class="bg-white p-6 shadow-md rounded-lg flex flex-col space-y-4 h-full">
      <h2 class="text-lg font-bold font-helvetica-neue text-peppercorn">AI Content Generation</h2>
      {/* if !selectedTrendId, show "Select a trend to generate content ideas." */}
      {/* if selectedTrendId: */}
      <>
        <p className="font-helvetica-neue">Content for: <span className="font-bold">{selectedTrendName}</span></p>
        <button class="bg-peppercorn text-white font-helvetica-neue py-2 px-4 rounded hover:bg-gray-700 disabled:opacity-50"
                onClick={handleGenerateContent} disabled={isLoading || !selectedTrendId}>
          {isLoading ? 'Generating...' : 'Generate Ideas'}
        </button>
        {/* if error, show error message */}
        {/* if generatedContent: display formatted content (subjects, body, themes) with copy-to-clipboard buttons */}
        {/* Example for one piece of content: */}
        {/* <div><h4>Email Subjects:</h4> {generatedContent.email_subject_lines.map(s => <p>{s} <CopyButton textToCopy={s} /></p>)} </div> */}
      </>
    </section>
    ```

- **Events Handled / Emitted:**
  - Handles: Click on "Generate Ideas" button. Clicks on "Copy" buttons (handled by `CopyButton` sub-component).
- **Actions Triggered (Side Effects):**
  - On "Generate Ideas" click: Sets `isLoading` to true. Calls an API service function (e.g., `apiClient.generateContentForTrend(selectedTrendId)`).
    - On success: Updates `generatedContent` state, sets `isLoading` to false.
    - On error: Sets `error` state, sets `isLoading` to false.
- **Styling Notes:**
  - Panel styling as per mockup.
  - "Generate Ideas" button styled as a primary Mailchimp CTA (Peppercorn background).
  - Display of generated content should be clean and readable, with clear "Copy" buttons (using Lucide Icons).
- **Accessibility Notes:**
  - `<section>` landmark with `aria-labelledby` pointing to `<h2>`.
  - Loading state announced (`aria-live`, `aria-busy`).
  - Generated content sections should be clearly delineated. Copy buttons need accessible labels.
  - Ensure button is disabled correctly when `isLoading` or no `selectedTrendId`.

This covers the foundational components. More specific components like `TrendFilterControls` or `CopyButton` would be detailed using the same template as development progresses.

Next, I'll elaborate on the "State Management Strategy (Detailed)".

## State Management In-Depth

This section elaborates on the state management strategy for the Mailchimp Marketing Trends Engine MVP, focusing on the use of React Context API and Hooks, and considering when a lightweight global state manager might become necessary.

### Chosen Solution & Decision Guide

- **Primary Solution (MVP): React Context API / Hooks**
  - **Rationale:** As specified in the Main Architecture Document and the project brief, the MVP prioritizes simplicity and leveraging built-in React features. For the three-panel dashboard, the state sharing needs are anticipated to be manageable with Context API, especially for:
    - Sharing the currently selected trend data between the `TrendFeedPanel`, `TrendDetailsPanel`, and `AiContentPanel`.
    - Managing filter state that affects the `TrendFeedPanel` and potentially influences data refetching.
- **Decision Guide for State Location:**
  - **Local Component State (`useState`, `useReducer`):**
    - **Use Case:** UI-specific state that doesn't need to be shared (e.g., open/close state of a dropdown if not part of `shadcn/ui`'s built-in behavior, input values within a form before submission if not managed by a form library, loading/error states for component-specific data fetching).
    - **MUST be the default choice.**
  - **React Context API:**
    - **Use Case:** Data that needs to be shared across a subtree of components without prop drilling. Ideal for:
      - The currently selected trend object (`selectedTrend`).
      - The list of fetched trends if multiple sibling components need to react to it without a common parent easily passing props.
      - Filters state if multiple components need to read or update them.
      - Theme or user preference settings (though less critical for MVP).
    - **Specific Contexts Needed (Identified for MVP):**
            1. `TrendsDataContext`: To provide the list of fetched trends, loading state, error state for trends, and current filters. It might also hold functions to update filters and refetch trends.
            2. `SelectedTrendContext`: To provide the details of the currently selected trend (`TrendDetailResponse | null`), its loading/error state, and potentially a function to set the selected trend ID (which would then trigger a fetch for its details).
    - **MUST be used for localized state not suitable for prop drilling but not complex enough or globally pervasive to warrant Zustand/Jotai immediately.**
  - **Lightweight Global State Manager (Zustand or Jotai - Post-MVP or if compelling need arises):**
    - **Use Case:** If state becomes truly global (needed by many disconnected parts of the app), state logic becomes very complex (many interdependent actions/reducers), or performance issues arise from Context updates causing excessive re-renders in large trees. Examples: User authentication state (though for MVP, this might be simple enough for Context if user login is added), application-wide notification system.
    - **Justification for MVP:** Currently, the identified shared state (trends list, selected trend, filters) seems manageable with well-structured Contexts. If, for instance, the AI Content Generation panel needed to interact with a global "user credits" system, or if many more top-level features were added that all relied on the same slice of state, then a global manager would be re-evaluated.
    - **Redux is explicitly avoided for MVP complexity.**

### Context API Usage

#### 1\. `TrendsDataContext`

- **Purpose:** Manages the state related to the list of trends displayed in the `TrendFeedPanel`, including filters, loading/error states, and the trend data itself.
- **Source File:** `frontend/contexts/TrendsDataContext.tsx`
- **State Shape (Interface/Type):**

    ```typescript
    // In lib/types.ts or co-located
    interface TrendFilters {
      category: string | null;
      sentiment: string | null;
      // Potentially sortBy, order, limit, offset if client-driven
    }

    interface TrendsDataContextState {
      trends: TrendListItem[];
      isLoadingTrends: boolean;
      trendsError: string | null;
      filters: TrendFilters;
      availableCategories: string[]; // For populating filter dropdown
      // Functions
      updateFilters: (newFilters: Partial<TrendFilters>) => void;
      refetchTrends: () => void; // Could be triggered by filter changes
      setTrendsData: (data: TrendListItem[], total: number) => void; // If data fetched outside
      setTrendsLoading: (loading: boolean) => void;
      setTrendsError: (error: string | null) => void;
    }
    ```

- **Provider Logic:**
  - The provider (`TrendsDataProvider`) will likely use `useState` and `useReducer` internally to manage the state.
  - It will contain a `useEffect` hook to fetch initial trends based on default filters when the provider mounts.
  - `updateFilters` will change the filter state and potentially trigger a `refetchTrends`.
  - `refetchTrends` will make an API call (e.g., `apiClient.getTrends(filters)`) and update `trends`, `isLoadingTrends`, and `trendsError`.
- **Consumed By:**
  - `TrendFeedPanel`: To display trends and filter controls.
  - Potentially other components if they need access to the raw trends list or filter state.

#### 2\. `SelectedTrendContext`

- **Purpose:** Manages the state of the currently selected trend, providing its detailed information to `TrendDetailsPanel` and `AiContentPanel`.
- **Source File:** `frontend/contexts/SelectedTrendContext.tsx`
- **State Shape (Interface/Type):**

    ```typescript
    // In lib/types.ts or co-located
    interface SelectedTrendContextState {
      selectedTrendDetails: TrendDetailResponse | null;
      isLoadingDetails: boolean;
      detailsError: string | null;
      selectedTrendId: string | null; // Keep track of the ID that was selected
      // Functions
      selectTrend: (trendId: string | null) => void; // Clears details if null, fetches if ID
    }
    ```

- **Provider Logic:**
  - The provider (`SelectedTrendProvider`) will use `useState` for its internal state.
  - The `selectTrend` function will update `selectedTrendId`. If an ID is provided, it will trigger a `useEffect` hook that depends on `selectedTrendId`.
  - This `useEffect` hook will:
    - Set `isLoadingDetails` to true, `detailsError` to null.
    - Call the API (e.g., `apiClient.getTrendDetails(trendId)`) to fetch details.
    - On success, update `selectedTrendDetails` and set `isLoadingDetails` to false.
    - On error, update `detailsError` and set `isLoadingDetails` to false.
    - If `trendId` is null, it clears `selectedTrendDetails`, `isLoadingDetails`, and `detailsError`.
- **Consumed By:**
  - `TrendFeedPanel`: Calls `selectTrend(trend.id)` when a `TrendCard` is clicked.
  - `TrendDetailsPanel`: Displays `selectedTrendDetails`, `isLoadingDetails`, `detailsError`.
  - `AiContentPanel`: Uses `selectedTrendId` and `selectedTrendDetails.name` (or similar) to know which trend to generate content for.

### Potential Lightweight Global State Manager (if deemed necessary)

- **Scenario for Re-evaluation:** If state interdependencies become highly complex across more than 2-3 contexts, or if performance due to context re-renders becomes an issue, or if features like real-time updates, extensive caching needs, or complex optimistic UI updates are introduced that are better handled by dedicated libraries.
- **Preferred Options (if needed):**
    1. **Zustand:**
          - **Justification:** Minimalistic, unopinionated, simple API, uses hooks, less boilerplate than Redux. Good for scaling up from Context without a steep learning curve.
          - **Usage Pattern:** Define a store (e.g., `frontend/store/useGlobalStore.ts`) with state and actions. Components would use the hook `const { data, actions } = useGlobalStore();`.
    2. **Jotai:**
          - **Justification:** Atomic state management, also minimalistic and hook-based. Scales well from `useState` paradigm. Good for scenarios where you want to isolate state updates finely.
          - **Usage Pattern:** Define atoms (e.g., `frontend/store/atoms.ts`). Components use hooks like `useAtom(myAtom)` to read/write state.
- **Current Stance:** For MVP, React Context API is the chosen approach. The above are considerations for future evolution if justified by increasing complexity.

This detailed state management strategy should provide a good balance of simplicity for the MVP while allowing for targeted sharing of data between the key panels of the application.

Next, I'll define the "Data Fetching and Caching Strategy."

## API Interaction Layer

This section details how the frontend application will fetch data from the backend API, manage loading and error states, and handle client-side caching if applicable for the MVP.

### Client/Service Structure

- **HTTP Client Setup:**

  - **Tool:** Native `Workspace` API available in modern browsers (and Node.js environments like Next.js Server Components/Route Handlers). For client-side components, `Workspace` will be used directly.
  - **Configuration Location:** A dedicated utility module, `frontend/lib/apiClient.ts`, will centralize API interaction logic.
  - **Base URL:** The backend API base URL (`/api/v1`) will be configurable via an environment variable `NEXT_PUBLIC_API_URL` (e.g., `http://localhost:8000/api/v1` for local development against the FastAPI backend).
  - **Default Headers:** Standard headers like `Content-Type: 'application/json'` and `Accept: 'application/json'` will be used for requests.
  - **Interceptors:** While native `Workspace` doesn't have interceptors like Axios, wrapper functions in `apiClient.ts` will handle:
    - Prepending the base URL.
    - Adding any necessary default headers.
    - Standardizing response handling (e.g., parsing JSON, basic error shaping).
    - Auth token injection (Post-MVP: if authentication is added, this module would be responsible for retrieving the token from state/storage and adding it to requests).

- **Service Definitions (Conceptual in `apiClient.ts`):**
    The `apiClient.ts` module will export functions for each backend API endpoint interaction.

    ```typescript
    // frontend/lib/apiClient.ts
    import { TrendListItem, TrendDetailResponse, GeneratedContentSchema, TrendFilters } from './types';

    const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || '/api/v1'; // Default for same-origin deployment

    async function WorkspaceApi<T>(url: string, options: RequestInit = {}): Promise<T> {
      const response = await Workspace(`${API_BASE_URL}${url}`, {
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
          ...options.headers,
        },
        ...options,
      });

      if (!response.ok) {
        // Attempt to parse error response from backend
        let errorMessage = `API Error: ${response.status} ${response.statusText}`;
        try {
          const errorBody = await response.json();
          errorMessage = errorBody.detail || errorMessage;
        } catch (e) {
          // Ignore if error body is not JSON or empty
        }
        throw new Error(errorMessage);
      }
      // For 204 No Content or similar, response.json() might fail
      if (response.status === 204) {
        return undefined as T;
      }
      return response.json() as Promise<T>;
    }

    // --- Trend Endpoints ---
    export const getTrends = async (filters?: TrendFilters): Promise<{ trends: TrendListItem[], total_count: number }> => {
      const queryParams = new URLSearchParams();
      if (filters?.category) queryParams.append('category', filters.category);
      if (filters?.sentiment) queryParams.append('sentiment', filters.sentiment);
      // Add other filters like sort_by, order, limit, offset as needed

      return WorkspaceApi<{ trends: TrendListItem[], total_count: number }>(`/trends?${queryParams.toString()}`);
    };

    export const getTrendDetails = async (trendId: string): Promise<TrendDetailResponse> => {
      return WorkspaceApi<TrendDetailResponse>(`/trends/${trendId}`);
    };

    // --- LLM Content Generation Endpoint ---
    export const generateContentForTrend = async (trendId: string): Promise<{ trend_id: string, trend_name: string, generated_content: GeneratedContentSchema }> => {
      return WorkspaceApi<{ trend_id: string, trend_name: string, generated_content: GeneratedContentSchema }>(
        `/trends/${trendId}/generate-content`,
        { method: 'POST' }
      );
    };
    ```

### Data Fetching Strategy

- **React Server Components (RSC) for Initial Load:**
  - The main dashboard page (`frontend/app/(dashboard)/page.tsx`) can be a Server Component.
  - It can directly `await` data fetching functions (e.g., initial list of trends using `getTrends()` from `apiClient.ts`) on the server during rendering.
  - This data can then be passed as props to client components (`TrendFeedPanel`, etc.) that hydrate on the client.
  - **Benefit:** Reduces client-side JavaScript for initial render, improves perceived performance, good for SEO if this page were public.
- **Client Components for Dynamic Interactions:**
  - Components requiring user interaction to fetch or re-fetch data (e.g., applying filters, selecting a trend to view details, generating AI content) will be Client Components (`"use client";`).
  - These components will use `useEffect` hooks in conjunction with state management (`useState`, `useContext`) to trigger API calls via `apiClient.ts` functions.
  - **Example (Fetching Trend Details in `SelectedTrendContext`):**

        ```typescript
        // In SelectedTrendContext.tsx
        useEffect(() => {
          if (selectedTrendId) {
            setIsLoadingDetails(true);
            getTrendDetails(selectedTrendId)
              .then(data => {
                setSelectedTrendDetails(data);
                setDetailsError(null);
              })
              .catch(err => {
                setDetailsError(err.message);
                setSelectedTrendDetails(null);
              })
              .finally(() => setIsLoadingDetails(false));
          } else {
            setSelectedTrendDetails(null); // Clear details if no ID
          }
        }, [selectedTrendId]); // Re-Workspace on ID change
        ```

- **Data Caching/Revalidation (MVP):**
  - **RSC Data Caching:** Next.js provides built-in data caching for `Workspace` requests made in Server Components. We can leverage this with appropriate `cache` options or revalidation strategies (e.g., time-based revalidation) if data freshness is critical and server-side fetching is used extensively.
    - `Workspace(url, { next: { revalidate: 3600 } }) // Revalidate every hour`
  - **Client-Side Caching:** For MVP, complex client-side caching libraries like SWR or TanStack Query (React Query) are **not planned** to maintain simplicity.
    - Basic caching can be achieved by storing fetched data in React Context or component state. Data is re-fetched when dependencies change (e.g., filters, selected ID).
    - If API responses are large and frequently re-used without change, or if optimistic updates/background revalidation become crucial post-MVP, then SWR/TanStack Query would be evaluated.
- **Managing Loading and Error States:**
  - Each data-fetching operation (whether in RSC or Client Components) will manage its own loading and error states.
  - Typically, boolean flags (`isLoading`, `isSubmitting`) and string/null states (`error`) will be used.
  - These states will be used to conditionally render UI elements:
    - Loading indicators (e.g., spinners, shimmer effects using `shadcn/ui` Skeleton component).
    - Error messages (e.g., using `shadcn/ui Alert` or inline text).
    - "No data" or empty states.
  - Context providers (e.g., `TrendsDataContext`, `SelectedTrendContext`) will expose these loading/error states alongside the data they manage, so consuming components can react appropriately.

### Error Handling & Retries (Frontend)

- **Global Error Handling:**
  - The `WorkspaceApi` wrapper in `apiClient.ts` centralizes basic error shaping.
  - For MVP, there won't be a global UI error banner triggered by default from all API errors. Instead, errors will primarily be handled by the specific context or component that initiated the API call.
  - If a truly global, unrecoverable error occurs (e.g., API completely down), Next.js error pages (`error.tsx`) can be used.
- **Specific Error Handling:**
  - Components and Contexts consuming API functions from `apiClient.ts` will use `.catch()` blocks or `try/catch` with `async/await` to handle errors.
  - The `error` state within these components/contexts will be updated with a user-friendly message derived from the error.
  - UI will then display this error (e.g., "Failed to load trends. Please try again.", "Could not generate content ideas.").
- **Retry Logic:**
  - **Client-side automatic retries are NOT planned for MVP** to maintain simplicity.
  - Users can manually trigger a re-fetch (e.g., a "Retry" button displayed alongside an error message, or by simply trying the action again like reapplying filters).
  - If specific endpoints are known to be flaky and would benefit from automatic retries post-MVP, a library like `Workspace-retry` or a custom wrapper around `Workspace` could be introduced, applied selectively to idempotent GET requests.

This API interaction strategy prioritizes leveraging Next.js features and native browser APIs for MVP, with clear extension points for more advanced caching or error handling if needed in the future.

Next, I will detail the "Frontend Routing."

## Routing Strategy

Navigation and routing within the Mailchimp Marketing Trends Engine frontend will be handled by the Next.js App Router, leveraging its file-system based routing capabilities.

- **Routing Library:** Next.js `~15.3.2` App Router.

### Route Definitions

The application is a Single-Page Application (SPA) centered around a main dashboard view. For the MVP, routing is minimal.

| Path Pattern | Component/Page (`frontend/app/...`) | Protection      | Notes                                                                                                                               |
| :------------- | :------------------------------------ | :-------------- | :---------------------------------------------------------------------------------------------------------------------------------- |
| `/`            | `app/(dashboard)/page.tsx`            | `Public (MVP)`  | The main and only view for the MVP. Displays the three-panel dashboard: Trend Feed & Filters, Trend Details, AI Content Generation. |
| *(other)* | `app/not-found.tsx` (default)         | `Public`        | Standard Next.js 404 page for any unmatched routes.                                                                                 |

**Detailed Explanation:**

1. **Root Path (`/`):**
      - **File:** `frontend/app/(dashboard)/page.tsx`
      - This is the entry point and the sole interactive page for the MVP. The `(dashboard)` segment is a route group, meaning it organizes files without affecting the URL path itself. So, accessing the application root effectively loads this page.
      - The `frontend/app/(dashboard)/layout.tsx` will define the three-column structure that hosts the `TrendFeedPanel`, `TrendDetailsPanel`, and `AiContentPanel`.
      - The `page.tsx` will be responsible for orchestrating these panels, potentially fetching initial data (like the list of trends) if implemented as a Server Component, and managing the state flow between them (likely via React Context as discussed).

**Future Considerations (Post-MVP):**
If the application were to expand with more distinct sections (e.g., user settings, different types of analytics dashboards), new routes would be added using the App Router's conventions:

- `/settings`: `app/settings/page.tsx`
- `/analytics/overview`: `app/analytics/overview/page.tsx`

### Route Guards / Protection

- **Authentication Guard:**
  - **MVP Scope:** For the MVP, user authentication is **not** a requirement. Therefore, all defined routes are effectively public.
  - **Post-MVP:** If authentication is introduced:
    - A mechanism like Next.js Middleware (`frontend/middleware.ts`) would be implemented.
    - This middleware would check for an authentication token (e.g., from an `HttpOnly` cookie or a secure client-side store).
    - If a route requires authentication and the user is not authenticated, the middleware would redirect them to a login page (e.g., `/login`).
    - The authentication status would likely be managed in a global state (e.g., `SessionContext` or a Zustand/Jotai store).
- **Authorization Guard (if applicable):**
  - **MVP Scope:** Not applicable as there are no distinct user roles or protected resources based on roles.
  - **Post-MVP:** If roles/permissions are introduced:
    - The Authentication Guard (e.g., middleware or HOCs/layout checks) would be extended.
    - After confirming authentication, it would check if the user's roles/permissions (obtained from their session/profile data) allow access to the requested route.
    - Unauthorized users (authenticated but lacking permissions) would be redirected to a "Forbidden" (403) page or a safe default page.

For the current MVP, the routing is straightforward, focusing on delivering the core dashboard experience on the root path.

Next, I'll specify the "Styling Conventions."

## Styling Conventions

Styling for the Mailchimp Marketing Trends Engine will be primarily managed by Tailwind CSS, with `shadcn/ui` providing unstyled, accessible base components. The overarching goal is to achieve "Mailchimp Harmony" by aligning the UI's look and feel with Mailchimp's established design language, as referenced in the `ui-ux-spec.md`, `Final-Mailchimp-Aligned-Dashboard-Mockup.png`, and the `515-Media-Mailchimp-User-Guide-REV2.pdf`.

### Tailwind CSS Configuration & Usage

- **Core Framework:** Tailwind CSS `~3.5.1`.
- **Configuration Files:**
  - `frontend/tailwind.config.js`: This is the central Tailwind configuration file. It will be used to:
    - Extend the default theme with Mailchimp-specific brand colors, fonts, and spacing.
    - Register any necessary Tailwind CSS plugins.
    - Configure `content` paths to ensure Tailwind scans all relevant files (`./app/**/*.{js,ts,jsx,tsx}`, `./components/**/*.{js,ts,jsx,tsx}`, etc.).
  - `frontend/postcss.config.mjs`: Standard PostCSS configuration for Tailwind CSS and Autoprefixer, typically provided by Next.js setup.
  - `frontend/styles/globals.css`:
    - Includes Tailwind's base, components, and utilities directives (`@tailwind base; @tailwind components; @tailwind utilities;`).
    - Defines any global base styles (e.g., default body background color, default font settings if not fully managed by Tailwind's theme).
    - Can house global CSS custom properties (variables) for the Mailchimp theme if needed, though direct theme extension in `tailwind.config.js` is preferred.
    - May contain a few global utility classes if absolutely necessary, but this should be minimized in favor of Tailwind's utility-first approach.
- **Usage Conventions:**
  - **Utility-First:** Styling will primarily be applied by composing utility classes directly in the JSX of React components.

        ```jsx
        <button className="bg-cavendish-yellow text-peppercorn font-helvetica-neue py-2 px-4 rounded hover:opacity-90">
          Click Me
        </button>
        ```

  - **`shadcn/ui` Customization:** Components from `shadcn/ui` will be added via its CLI. These components are unstyled by default but provide sensible structures and accessibility. They will be styled using Tailwind utility classes, either directly when used or by customizing their underlying parts if more complex reusable variants are needed.
  - **Responsive Design:** Tailwind's responsive prefixes (`sm:`, `md:`, `lg:`, `xl:`) will be used extensively to implement the responsive behaviors defined in the `ui-ux-spec.md`. Breakpoints from `ui-ux-spec.md` (Tailwind defaults) will be used.
  - **State Variants:** Tailwind's state variants (`hover:`, `focus:`, `disabled:`, `dark:`, etc.) will be used to style components in different states.
  - **No Custom CSS Files (Ideally):** For MVP, the aim is to achieve all styling with Tailwind utilities and `shadcn/ui`. If highly complex, non-reusable component-specific styles are needed that cannot be expressed cleanly with utilities, a co-located CSS Modules file could be considered as a last resort, but this is discouraged. The `@apply` directive should be used sparingly, primarily within `globals.css` for base component styles if absolutely necessary, not for creating custom utility-like classes.

### Mailchimp Design Harmony

- **Primary References:**
  - `Final-Mailchimp-Aligned-Dashboard-Mockup.png`: The key visual guide for layout, component appearance, and overall aesthetic.
  - `ui-ux-spec.md`: Contains specific details on color palette, typography, and styling principles derived from Mailchimp.
  - `515-Media-Mailchimp-User-Guide-REV2.pdf`: General inspiration for Mailchimp's UI patterns and feel.
- **Theme Integration in `tailwind.config.js`:**
  - **Colors:** The Mailchimp color palette (Cavendish Yellow `~#FFE01B`, Peppercorn `~#2E2E2E`, Light Grey `~#F5F6F5`, White `~#FFFFFF`, Subtle Yellow Tint `~#FFF8D1`, Border Grey `~#E0E0E0`, etc., from `ui-ux-spec.md`) will be added to `theme.extend.colors` in `tailwind.config.js`.

        ```javascript
        // frontend/tailwind.config.js
        module.exports = {
          theme: {
            extend: {
              colors: {
                'cavendish-yellow': '#FFE01B',
                'peppercorn': '#2E2E2E',
                'light-grey-bg': '#F5F6F5', // for page background
                'subtle-yellow-tint': '#FFF8D1', // for hover states
                'border-grey': '#E0E0E0',
                // ... other Mailchimp colors
              },
              fontFamily: {
                'helvetica-neue': ['Helvetica Neue', 'Arial', 'sans-serif'],
              },
            },
          },
          // ... other configurations
        };
        ```

  - **Typography:** The primary font, Helvetica Neue, will be defined in `theme.extend.fontFamily`. Default font sizes, weights, and line heights will be influenced by Mailchimp's typography, applied via utility classes. Base body font can be set in `globals.css`.
  - **Spacing:** Spacing utilities will be used to match the clean, uncluttered layout with adequate white space seen in the mockup and Mailchimp interfaces. Default spacing scale in Tailwind might be adjusted if necessary.
  - **Icons:** Lucide Icons (`lucide-react`) will be used and styled with Tailwind (color, size) to match Mailchimp's simple, clean icon style.
- **Component Styling:**
  - `shadcn/ui` components will serve as the structural and accessible base.
  - Their visual appearance (borders, backgrounds, typography, padding, rounded corners) will be customized using Tailwind utilities to precisely match the `Final-Mailchimp-Aligned-Dashboard-Mockup.png` and the Mailchimp aesthetic. For example, `shadcn/ui Button` will be styled to look like Mailchimp buttons (e.g., primary Peppercorn button).
  - Shadows, borders, and interactive states (hover, focus, active, selected) will emulate Mailchimp's subtle and clear visual cues.

By consistently applying these conventions, the frontend will achieve the desired "Mailchimp Harmony" while benefiting from the efficiency and maintainability of Tailwind CSS and `shadcn/ui`.

Next, I'll detail "Forms and User Input Handling."

## Forms and User Input Handling

This section details how forms (primarily for trend filtering in the MVP) will be managed, including validation and submission logic.

### Form Management

- **Primary Use Case (MVP):** The main form-like interface in the MVP is the "Trend Filters" section within the `TrendFeedPanel`. This includes:
  - Category dropdown (`shadcn/ui Select`).
  - Sentiment toggle/buttons (`shadcn/ui Toggle Group` or custom styled `Button`s).
- **State Management for Filters:**
  - The state of the filters (`activeFilters` object: `{ category: string | null, sentiment: string | null }`) will be managed by the `TrendsDataContext` as previously outlined.
  - Filter components (e.g., `TrendFilterControls.tsx` within `frontend/features/trend-filtering/`) will receive the current filter values as props and call the `onFilterChange` callback (from `TrendsDataContext`) when a user interacts with a filter control.
- **Libraries:**
  - For the MVP's simple filter controls, a dedicated form library like Formik or React Hook Form is **not deemed necessary**. Direct state management via React Context and `useState` within the filter components should suffice.
  - If more complex forms with extensive validation and submission logic were introduced post-MVP, React Hook Form would be the preferred choice due to its performance and hook-based API.
- **Component Implementation:**
  - `TrendFilterControls.tsx` will encapsulate the `shadcn/ui Select` for categories and `ToggleGroup` (or equivalent) for sentiment.
  - These `shadcn/ui` components will have their `value` prop bound to the corresponding property in `activeFilters` and their `onValueChange` (or similar) prop tied to functions that call `onFilterChange` with the updated filter value.

### Validation

- **Client-Side Validation (UX):**
  - **MVP Scope:** For the filter inputs, explicit client-side validation is minimal as they are selection-based (dropdown, toggles).
    - The category dropdown will only present valid categories fetched from the backend or a predefined list.
    - The sentiment toggle will only allow predefined sentiment values.
  - **General Approach (if text inputs were present):** If free-form text inputs were used (e.g., a search bar for trends Post-MVP), basic client-side validation (e.g., for non-empty, max length) would be implemented for immediate user feedback. This would involve:
    - `onChange` handlers updating local component state.
    - Displaying error messages near the input field (e.g., using `shadcn/ui` styling for helper text in an error state).
- **Server-Side Validation:**
  - All filter parameters sent to the backend API (`/api/v1/trends`) **must be validated by the backend**, as per the main Architecture Document. The frontend relies on the backend as the ultimate source of truth for data validity.
  - The frontend should gracefully handle any validation error responses from the backend (e.g., a 422 Unprocessable Entity), though for selection-based filters, this is less likely.

### Submission

- **Filter "Submission" (Applying Filters):**
  - Changes to filter controls (category dropdown, sentiment toggle) will trigger the `onFilterChange` callback provided by `TrendsDataContext`.
  - The `TrendsDataContext` will then:
        1. Update its internal `filters` state.
        2. Trigger a re-fetch of the trend list by calling `apiClient.getTrends()` with the new `filters`.
  - There is no explicit "Submit" button for filters; changes are applied reactively as the user interacts with the controls (debouncing might be added if re-fetching on every tiny change becomes an issue, but for select/toggle, it's usually acceptable).
- **AI Content Generation Trigger:**
  - The "Generate Ideas" button in the `AiContentPanel` acts as a form submission trigger.
  - **Pre-submission check:** The button will be disabled if no trend is selected (`selectedTrendId` is null) or if a generation request is already in progress (`isLoading` is true).
  - **Action:** On click, it calls the `apiClient.generateContentForTrend(selectedTrendId)` function.
  - Loading and error states specific to this action will be managed within `AiContentPanel`.

For the MVP, form handling is relatively simple due to the nature of the filter controls. The architecture is set up to manage this via context and direct API calls.

Next, I will elaborate on the "Frontend Testing Strategy."

## Frontend Testing Strategy

This section elaborates on the "Overall Testing Strategy" from the main `architecture.md`, providing frontend-specific details for testing the Next.js application, its components, hooks, and pages. The primary tools are Jest and React Testing Library (RTL).

- **Link to Main Overall Testing Strategy:** `docs/architecture.md#overall-testing-strategy`

### Component Testing

- **Scope:** Testing individual React components in isolation. This includes UI elements from `shadcn/ui` (if wrapped or heavily customized) and custom-built components (e.g., `TrendCard`, panel components like `TrendFeedPanel` with mocked props).
- **Tools:** Jest (`~29.8.0`) as the test runner and assertion library; React Testing Library (`~15.2.0`) for rendering components and interacting with them in a user-centric way.
- **Focus:**
  - **Rendering:** Verify components render correctly with different sets of props (e.g., presence/absence of data, different states).
  - **Interaction:** Simulate user events (clicks, input changes, selections) using RTL's `userEvent` library (preferred over `fireEvent` for more realistic interactions) and assert that the component behaves as expected (e.g., callbacks are called, internal state changes, UI updates).
  - **Accessibility (Basic):** Use `jest-axe` to run automated accessibility checks on rendered component output within tests to catch basic WCAG violations.
  - **Snapshot Testing:** To be used **sparingly** and only for very stable, purely presentational components where the DOM structure is complex and unlikely to change frequently. If used, snapshots must be committed and reviewed carefully on changes. Prefer explicit assertions about content and attributes.
- **Location:** Test files (`*.test.tsx` or `*.spec.tsx`) will be co-located with the component files they are testing (e.g., `frontend/components/ui/TrendCard.test.tsx`).
- **Example (`TrendCard.test.tsx` - Conceptual):**

    ```typescript
    import { render, screen } from '@testing-library/react';
    import userEvent from '@testing-library/user-event';
    import { TrendCard } from './TrendCard'; // Adjust import path
    import { axe } from 'jest-axe';

    const mockTrend = { id: '1', name: 'Test Trend', identified_date: new Date().toISOString(), score: 0.85, sentiment: 'positive', category: 'Tech', summary: 'A test trend.' };
    const mockOnSelect = jest.fn();

    describe('TrendCard', () => {
      it('renders trend information correctly', () => {
        render(<TrendCard trend={mockTrend} onSelect={mockOnSelect} />);
        expect(screen.getByText('Test Trend')).toBeInTheDocument();
        expect(screen.getByText(/Score: 0.85/)).toBeInTheDocument();
        // ... other assertions
      });

      it('calls onSelect with trendId when clicked', async () => {
        render(<TrendCard trend={mockTrend} onSelect={mockOnSelect} />);
        await userEvent.click(screen.getByRole('button', { name: /Test Trend/i })); // Assuming card acts like a button
        expect(mockOnSelect).toHaveBeenCalledWith('1');
      });

      it('should have no accessibility violations', async () => {
        const { container } = render(<TrendCard trend={mockTrend} onSelect={mockOnSelect} />);
        const results = await axe(container);
        expect(results).toHaveNoViolations();
      });
    });
    ```

### UI Integration/Flow Testing

- **Scope:** Testing the interaction of several components working together to fulfill a user flow or a significant part of a page's functionality. For MVP, this would involve testing how the three main panels (`TrendFeedPanel`, `TrendDetailsPanel`, `AiContentPanel`) interact via shared context.
- **Tools:** Jest and React Testing Library, with mocked context providers and API responses.
- **Focus:**
  - Data flow through components via props and context.
  - Conditional rendering based on shared state.
  - Ensuring actions in one component correctly update the state that affects other components.
  - Example Flow:
        1. Render the main dashboard page structure with mocked `TrendsDataContext` and `SelectedTrendContext`.
        2. Simulate applying a filter in `TrendFeedPanel`.
        3. Verify that `TrendsDataContext` reflects the filter change and that a (mocked) API call to fetch trends with new filters is made.
        4. Simulate selecting a trend in `TrendFeedPanel`.
        5. Verify that `SelectedTrendContext` is updated with the selected trend ID.
        6. Verify that `TrendDetailsPanel` receives and displays (mocked) details for the selected trend.
        7. Verify that `AiContentPanel` updates to reflect the selected trend context.
        8. Simulate clicking "Generate Ideas" in `AiContentPanel` and verify (mocked) API call and display of generated content.
- **Location:** Integration tests might be placed in a feature-specific test directory (e.g., `frontend/app/(dashboard)/__tests__/dashboard-integration.test.tsx`) or a top-level `frontend/tests/integration/`.

### End-to-End UI Testing Tools & Scope

- **Tools:** As defined in the main `architecture.md`, this is likely Playwright or Cypress if full E2E tests were in scope. **For MVP, full browser-based E2E tests are out of scope.** The focus is on comprehensive unit and integration tests using Jest/RTL.
- **MVP Scope:** Not applicable. If this changes, key user journeys would be defined here.

### Mocking API Calls

- **Strategy:** API calls made via `frontend/lib/apiClient.ts` will be mocked during unit and integration tests.
- **Method:** Use `jest.mock()` to mock the `apiClient.ts` module.

    ```typescript
    // In a test file (e.g., frontend/contexts/__tests__/TrendsDataContext.test.tsx)
    import * as apiClient from '@/lib/apiClient'; // Adjust path

    jest.mock('@/lib/apiClient'); // Mock the entire module

    const mockedGetTrends = apiClient.getTrends as jest.MockedFunction<typeof apiClient.getTrends>;
    // ... other mocked functions

    beforeEach(() => {
      mockedGetTrends.mockResolvedValue({ trends: [/* mock trend data */], total_count: 1 });
      // Set default mock implementations for other API calls
    });

    // In tests:
    // mockedGetTrends.mockResolvedValueOnce(...) // for specific responses
    // expect(mockedGetTrends).toHaveBeenCalledWith(...);
    ```

- This approach allows tests to control API responses, simulate loading/error states, and verify that correct parameters are passed to API functions without making actual network requests.

By focusing on strong component and integration testing with Jest and RTL, and thorough mocking of API interactions, the frontend for the MVP can achieve a high degree of quality and reliability.

Next, I will detail the "Accessibility (AX) Implementation Details."

## Accessibility (AX) Implementation Details

Ensuring the Mailchimp Marketing Trends Engine is accessible is a core requirement, targeting WCAG 2.1 Level AA compliance as outlined in the `ui-ux-spec.md`. The following technical implementation guidelines will be followed:

- **Semantic HTML:**
  - **Mandate:** Developers and AI agents **must** prioritize using HTML5 elements according to their intended semantic meaning. For example:
    - `<nav>` for navigation blocks.
    - `<main>` for the primary content area of the page.
    - `<aside>` for side panels like the "Trend Feed & Filters Panel".
    - `<section>` for distinct thematic groupings of content, each with an appropriate heading.
    - `<article>` for self-contained compositions like individual trend cards if they were more complex (for current `TrendCard`, a `div` with `role="button"` or `role="listitem"` might be more appropriate depending on context).
    - `<button>` for all interactive elements that trigger an action. `<a>` tags for navigation.
    - Headings (`<h1>` - `<h6>`) will be used hierarchically to structure content. The main dashboard title will be an `<h1>`. Panel titles will be `<h2>`.
  - Avoid using `div` or `span` for elements that have a more specific semantic counterpart.
- **ARIA Implementation:**
  - **Guideline:** ARIA (Accessible Rich Internet Applications) attributes will be used to enhance the accessibility of custom components and dynamic content where semantic HTML alone is insufficient.
  - **`shadcn/ui`:** These components generally come with good ARIA support out-of-the-box. Customizations should preserve or enhance this.
  - **Common Custom Components & ARIA Patterns (Examples):**
    - **Trend Card (`TrendCard.tsx`):** If it acts as an interactive button to select a trend, it should have `role="button"` and `tabindex="0"`. If part of a list of trends, list items might have `role="listitem"` within a container with `role="list"`. If it's a primary clickable entity, `aria-pressed` could indicate selection.
    - **Filter Controls (e.g., `shadcn/ui Select`, `ToggleGroup`):** These `shadcn/ui` components typically manage their own ARIA attributes (`aria-expanded`, `aria-controls`, `aria-checked`, `role="combobox"`, `role="radiogroup"`, etc.). Ensure labels are correctly associated using `<label htmlFor="...">` or `aria-labelledby`.
    - **Panels (`TrendFeedPanel.tsx`, etc.):** Each panel (`<aside>` or `<section>`) should have an accessible name, typically provided by its heading (e.g., an `<h2>` associated via `aria-labelledby`).
    - **Dynamic Content Updates & Notifications:**
      - Loading states: Use `aria-busy="true"` on regions being updated.
      - Error messages or success notifications: Use `aria-live="polite"` (for non-critical updates) or `aria-live="assertive"` (for critical updates) on the message container to ensure screen readers announce them. `shadcn/ui Toast` or `Alert` components should handle this.
  - **Reference:** ARIA Authoring Practices Guide (APG) will be consulted for complex custom widgets if any are developed beyond `shadcn/ui`.
- **Keyboard Navigation:**
  - **Mandate:** All interactive elements (buttons, links, form controls, custom components acting as controls) **must** be focusable and operable using only the keyboard.
  - **Focus Order:** The focus order must be logical and intuitive, generally following the visual layout of the page (left-to-right, top-to-bottom for LTR languages).
  - **Standard Interactions:** Standard HTML controls (`<button>`, `<input>`, `<select>`) and `shadcn/ui` components will generally have correct keyboard behavior.
  - **Custom Interactive Elements (e.g., `TrendCard`):** If a `div` is made interactive, it must have `tabindex="0"` to be included in the focus order and must respond to `Enter` and/or `Space` keys as a button would.
- **Focus Management:**
  - **Initial Page Load:** Focus should ideally be set to the main content area or the first interactive element after the page title/header.
  - **Modals/Dialogs (Post-MVP):** If modals are introduced, focus **must** be trapped within the modal. When the modal is opened, focus moves to the first focusable element within it (or the modal container itself). Upon closing, focus **must** return to the element that triggered the modal. `shadcn/ui Dialog` handles this.
  - **Dynamic Content Changes:** When new content appears (e.g., AI-generated content), if it's the primary result of an action, consider moving focus to the new content or a heading for it, especially if it appears off-screen.
  - **Route Transitions (MVP - Single Page):** Not highly relevant for the MVP's single-page structure. Post-MVP, on route changes, focus should be moved to the main content area or `<h1>` of the new page.
- **Color Contrast & Legibility:**
  - The color palette defined in `ui-ux-spec.md` (Cavendish Yellow, Peppercorn, etc.) must be used in combinations that meet WCAG 2.1 AA contrast ratios (4.5:1 for normal text, 3:1 for large text and UI components/graphical objects). Tools like WebAIM Contrast Checker will be used for verification.
  - Font (Helvetica Neue) and sizes specified in `ui-ux-spec.md` must ensure legibility.
- **Alternative Text for Images:**
  - All meaningful images (`<img>`, SVGs acting as images) **must** have descriptive `alt` text (e.g., Mailchimp logo).
  - Decorative images should have an empty `alt=""`.
  - Icons that convey meaning (e.g., a "copy" icon button) must have an accessible name, either via `aria-label` on the button or visually hidden text. Lucide Icons used with `shadcn/ui Button` (as an icon button) should ensure this.
- **Forms & Labels:**
  - All form inputs (`<input>`, `<select>`, `<textarea>`) **must** have associated `<label>` elements, correctly linked using the `for` attribute or by wrapping the input. `shadcn/ui Label` should be used.
- **Testing Tools for AX:**
  - **Automated:**
    - `jest-axe`: Will be integrated into component tests to catch violations during development. Tests will fail on new violations.
    - Browser extensions like **Axe DevTools** or **Lighthouse** (accessibility audit) will be used for spot-checking during development and before "releases."
  - **Manual:**
    - Keyboard-only navigation testing for all interactive elements and user flows.
    - Screen reader testing (e.g., NVDA, VoiceOver, JAWS - one primary for MVP) for critical user flows: viewing trends, filtering, selecting a trend, generating and copying content.
    - Zooming page to 200% to check for content overlap or loss.
    - Checking color contrast with browser developer tools or dedicated plugins.

By embedding these practices into the development workflow, the aim is to create an inclusive experience for all users.

Next, I'll cover "Performance Considerations."

## Performance Considerations

Ensuring a performant frontend is crucial for user satisfaction and usability. The following strategies will be employed for the Mailchimp Marketing Trends Engine:

- **Image Optimization:**

  - **Formats:** Prefer modern image formats like WebP for bitmaps where browser support allows, with fallbacks if necessary. SVGs will be used for icons (via Lucide Icons) and logos where appropriate, as they are scalable and lightweight.
  - **Responsive Images:** Use Next.js's `<Image>` component (`next/image`). It provides automatic image optimization, resizing, format conversion (e.g., to WebP), and generation of `srcset` for responsive images, serving appropriately sized images based on the viewport.
  - **Lazy Loading:** The `next/image` component handles lazy loading by default for images below the fold.
  - **Implementation Mandate:** All significant static images (e.g., mockups if embedded, illustrations) MUST use the `<Image>` component from Next.js. SVGs for icons.

- **Code Splitting & Lazy Loading:**

  - **Route-based Code Splitting:** Next.js App Router automatically performs code splitting for each route (page). Only the JavaScript necessary for the current page is loaded initially.
  - **Component-level Lazy Loading:** For large components that are not critical for the initial paint or are conditionally rendered (e.g., a complex chart library if it were very heavy and not always visible), dynamic imports (`React.lazy` with `Suspense`, or Next.js `next/dynamic`) WILL be used.

      ```typescript
      import dynamic from 'next/dynamic';
      const HeavyChartComponent = dynamic(() => import('@/components/ui/HeavyChartComponent'), {
        suspense: true, // Optional: use with <Suspense fallback={...}>
        ssr: false // Optional: if component is client-side only
      });
        ```

  - **Implementation Mandate:** Leverage Next.js's built-in route-based splitting. For any non-trivial component that is not immediately visible or is resource-intensive, evaluate and implement dynamic loading.

- **Minimizing Re-renders:**

  - **React.memo:** For presentational components that render frequently with the same props, `React.memo` will be used to prevent unnecessary re-renders.
  - **useCallback & useMemo:** For memoizing functions and values passed as props to memoized child components, or for expensive calculations within components.
  - **Optimized Selectors (if using global state manager post-MVP):** If Zustand/Jotai or similar is adopted, selectors will be designed to be efficient and memoized where appropriate (e.g., Reselect with Redux, or similar patterns for Zustand/Jotai).
  - **Context API Selectivity:** When using React Context, consuming components should select only the parts of the context value they need, or use `useContextSelector` (if a library providing it is adopted) to avoid re-renders when unrelated parts of the context change. For MVP with simple contexts, this might be less critical but good to keep in mind.
  - **Implementation Mandate:** Be mindful of prop equality. Avoid passing new object/array literals or inline functions as props directly in render methods to memoized components, as this breaks memoization.

- **Debouncing/Throttling:**

  - **Use Case:** For event handlers that can fire rapidly, such as search input or window resize (though less relevant for MVP's fixed layout). For MVP, filter changes directly trigger re-fetches; if this proves too chatty with many filter options, debouncing could be applied to the `onFilterChange` handler in `TrendsDataContext`.
  - **Implementation Mandate:** If frequent API calls due to rapid user input (e.g., typing in a search box post-MVP) cause performance issues, use a utility like `lodash.debounce` or a custom hook to limit the rate of API calls. A debounce time of 300-500ms is typical.

- **Virtualization (for long lists):**

  - **Use Case:** If the "Trend Feed" panel is expected to display hundreds or thousands of trend cards simultaneously, virtualization will be necessary to maintain performance by only rendering the items visible in the viewport.
  - **Libraries:** TanStack Virtual (React Virtual) or `react-window`.
  - **Implementation Mandate:** If the number of trend items regularly exceeds \~100 and performance degradation is observed during scrolling, virtualization MUST be implemented for the trend list.

- **Caching Strategies (Client-Side):**

  - **Next.js Data Cache (for RSC):** As mentioned in API Interaction, `Workspace` requests in Server Components benefit from Next.js's built-in caching. Use `revalidate` options to control freshness.
  - **Browser HTTP Caching:** Static assets generated by `next build` (JS/CSS bundles with content hashes) will be served with long-cache headers by the hosting platform (e.g., Vercel, Netlify). HTML pages will have cache headers that encourage revalidation. This is largely handled by Next.js and the deployment platform.
  - **Service Workers (PWA - Post-MVP):** Not in scope for MVP. If PWA capabilities are added later, a service worker would be implemented to cache the application shell and key static assets for offline access and faster loads.

- **Bundle Analysis:**

  - **Tool:** `@next/bundle-analyzer`.
  - **Usage:** Periodically analyze the production JavaScript bundle to identify large modules or unnecessary dependencies that could be optimized, code-split, or removed.
  - **Implementation Mandate:** Run bundle analysis before major "releases" or if performance issues are suspected.

- **Performance Monitoring Tools:**

  - **Browser DevTools:** Performance tab, Lighthouse audit (especially for Core Web Vitals - LCP, FID/INP, CLS).
  - **WebPageTest:** For more in-depth analysis from different locations/devices.
  - **Implementation Mandate:** Use Lighthouse audits regularly during development. Aim for green scores (90+) on performance. Profile using DevTools to identify specific bottlenecks in component rendering or script execution.

- **Minimize Client-Side JavaScript:**

  - Leverage Next.js Server Components where possible for logic that doesn't require client-side interactivity or browser APIs, reducing the amount of JavaScript shipped to the client.
  - Be judicious about adding client-side dependencies.

These performance considerations will guide development to ensure the dashboard is fast and responsive.

The sections "Internationalization (i18n) and Localization (l10n) Strategy" and "Feature Flag Management" are not primary requirements for this MVP based on the provided documents. I will mark them as "Not applicable for MVP" but include the template structure in case this changes.

## Internationalization (i18n) and Localization (l10n) Strategy

Internationalization is not a requirement for the Mailchimp Marketing Trends Engine MVP at this time. The application will be developed in English (US) only.

- **Requirement Level:** Not Required for MVP.
- **Chosen i18n Library/Framework:** N/A
- **Translation File Structure & Format:** N/A
- **Translation Key Naming Convention:** N/A
- **Process for Adding New Translatable Strings:** N/A
- **Handling Pluralization:** N/A
- **Date, Time, and Number Formatting:** Default browser/JavaScript formatting for US English locale will be used (e.g., `Date.toLocaleDateString()` without specific locale params implies user's default, which is acceptable for MVP).
- **Default Language:** `en-US`
- **Language Switching Mechanism (if applicable):** N/A

## Feature Flag Management

Feature flags are not a primary architectural concern for the Mailchimp Marketing Trends Engine MVP at this time. All features developed for the MVP will be enabled by default.

- **Requirement Level:** Not Required for MVP.
- **Chosen Feature Flag System/Library:** N/A
- **Accessing Flags in Code:** N/A
- **Flag Naming Convention:** N/A
- **Code Structure for Flagged Features:** N/A
- **Strategy for Code Cleanup (Post-Flag Retirement):** N/A
- **Testing Flagged Features:** N/A

Next, I will address "Frontend Security Considerations."

## Frontend Security Considerations

This section highlights mandatory frontend-specific security practices for the Mailchimp Marketing Trends Engine, complementing the main Architecture Document's security section. Adherence by developers and AI agents is crucial.

- **Cross-Site Scripting (XSS) Prevention:**
  - **Framework Reliance:** React's JSX auto-escaping of dynamic content rendered within `{}` **must** be relied upon. This is the primary defense against XSS when rendering data from the API or user-generated content (though the latter is not a direct input in MVP).
  - **Explicit Sanitization:** Avoid using `dangerouslySetInnerHTML`. If, in an extreme and unlikely post-MVP scenario, it becomes necessary, the content **must** be sanitized using a robust library like DOMPurify with a strict configuration. This is not anticipated for MVP.
  - **`shadcn/ui` components:** These are generally safe as they are built with React.
  - **Content Security Policy (CSP):** A CSP will be primarily enforced via HTTP headers set by the backend reverse proxy or CDN/hosting platform (as per main Architecture Document, if applicable for final deployment beyond local k3s). The frontend should avoid practices that would require overly permissive CSPs (e.g., inline scripts without nonces, `eval()`). For MVP on local k3s, a formal CSP header might not be configured, but secure coding practices remain.
- **Cross-Site Request Forgery (CSRF) Protection:**
  - **Mechanism:** The backend is a FastAPI application. If it uses session/cookie-based authentication (post-MVP), it would need to implement CSRF protection (e.g., synchronizer token pattern). The frontend would then need to ensure this token is included in state-changing requests.
  - **MVP Scope:** The backend API `/api/v1` is stateless for MVP (no user sessions from the frontend's perspective). Frontend requests are primarily GET, or POST for AI content generation which is non-user-state-changing in a CSRF-exploitable way. Thus, client-side CSRF token handling is not a direct concern for MVP. If auth is added, this needs re-evaluation.
- **Secure Token Storage & Handling:**
  - **MVP Scope:** No client-side user authentication tokens are managed in the MVP.
  - **Post-MVP:** If JWTs or other client-side tokens are introduced for user authentication:
    - **Storage Mechanism:** Tokens **must not** be stored in `localStorage`. Preferred options are in-memory (e.g., React state/context, Zustand/Jotai store, cleared on tab/browser close) or, if session persistence across tabs/reloads is needed without `HttpOnly` cookies, `sessionStorage` (less secure than in-memory for XSS but better than `localStorage`). `HttpOnly` cookies set by the backend are the most secure for web.
    - **Token Refresh:** Interceptors in `apiClient.ts` would handle 401 errors to trigger a token refresh mechanism against a backend refresh endpoint.
- **Third-Party Script Security:**
  - **Policy (MVP):** The MVP aims to use minimal third-party scripts directly injected into the HTML. Dependencies are primarily NPM packages (Next.js, React, Tailwind, Lucide, Chart.js via `shadcn/ui` or direct import).
  - **Chart.js (if used):** Will be imported as an NPM module, not via CDN script tag.
  - **Post-MVP:** If any third-party scripts for analytics, etc., are added, they must be vetted. Load via NPM if possible, or use `async/defer` and Subresource Integrity (SRI) if from a CDN.
- **Client-Side Data Validation:**
  - **Purpose:** Client-side validation is for UX improvement (immediate feedback) ONLY. For MVP filters, this is minimal as selections are constrained.
  - **Mandate:** **All critical data validation MUST occur server-side** (as defined in the main Architecture Document). The frontend must not assume client-side validation is sufficient for security.
- **Preventing Clickjacking:**
  - **Mechanism:** Primarily defended by `X-Frame-Options: DENY` or `SAMEORIGIN`, or `Content-Security-Policy: frame-ancestors 'self'` HTTP headers. These should be set by the deployment platform or reverse proxy (Post-MVP). The application itself is not designed to be embedded in iframes from other origins.
- **API Key Exposure (for client-side consumed services):**
  - **MVP Scope:** The frontend does not directly consume external services requiring API keys. All such calls (Jina, Claude) are proxied through the backend.
  - **Post-MVP:** If a service like Google Maps JS SDK were used directly on the client, its API key **must** be restricted (e.g., by HTTP referrer, IP address, API endpoint restrictions) via the service provider's console.
- **Secure Communication (HTTPS):**
  - **Mandate:** All communication between the frontend and the backend API (`/api/v1`) **must** use HTTPS in any non-local/staging/production environment.
  - **Local Development (Colima/k3s):** Communication might be HTTP internally within the k3s cluster or to `localhost`. If exposing the app externally for demo (e.g., via ngrok), ngrok would provide HTTPS.
  - **Mixed Content:** Forbidden. All assets must be loaded over HTTPS if the page is HTTPS.
- **Dependency Vulnerabilities:**
  - **Process:** `pnpm audit` will be used to check for vulnerabilities in frontend dependencies (`package.json`).
  - **CI Integration:** `pnpm audit --audit-level=high` should be integrated into the CI pipeline. High/critical vulnerabilities **must** be addressed before merging to `develop` or `main`, or a documented exception made.
  - Regularly update dependencies using `pnpm update`.

By following these guidelines, we aim to mitigate common frontend security risks.

Finally, I'll cover "Browser Support and Progressive Enhancement."

## Browser Support and Progressive Enhancement

This section defines the target browsers for the Mailchimp Marketing Trends Engine and the strategy for ensuring a consistent experience.

- **Target Browsers:**
  - Latest 2 stable versions of:
    - Google Chrome
    - Mozilla Firefox
    - Apple Safari (macOS and iOS)
    - Microsoft Edge (Chromium-based)
  - Internet Explorer (any version) is **NOT** supported.
  - Mobile responsiveness is required as per `ui-ux-spec.md`, so modern mobile versions of the above browsers are implicitly included.
- **Polyfill Strategy:**
  - **Mechanism:** Next.js automatically includes polyfills needed for its core functionality based on browser targets (e.g., for `Workspace`, Promises, `Object.assign`). The framework aims to support modern browsers, and its build process handles much of this.
  - `core-js`: While Next.js handles many polyfills, if specific JavaScript features are used that are not covered and are required by the target browser matrix (unlikely with the "latest 2 stable versions" target), `core-js` could be added, but it's not anticipated as a primary need.
  - **Specific Polyfills:** None anticipated for MVP given the browser targets and Next.js capabilities.
- **JavaScript Requirement & Progressive Enhancement:**
  - **Baseline:** Core application functionality of the Mailchimp Marketing Trends Engine (displaying trends, filtering, visualizations, AI content generation) **REQUIRES JavaScript enabled** in the browser. It is a single-page application built with React/Next.js.
  - **No-JS Experience:** A functional no-JavaScript experience is **not a goal for the MVP**. Users with JavaScript disabled will likely see a blank page or a basic HTML shell without content or interactivity. If server-side rendering via RSCs provides some initial HTML, it might be visible but not interactive.
  - **Progressive Enhancement:** While the baseline requires JS, the principle of progressive enhancement will be applied in terms of ensuring the application works well on a range of device capabilities within the supported browsers (e.g., handling different screen sizes gracefully).
- **CSS Compatibility & Fallbacks:**
  - **Tooling:** Tailwind CSS relies on PostCSS, and Next.js integrates Autoprefixer. Autoprefixer will be configured (typically by default in Next.js) to add necessary vendor prefixes for CSS properties to ensure compatibility across the target browsers.
  - **Feature Usage:** Modern CSS features (e.g., Flexbox, Grid) that are well-supported by the target browsers will be used. If any cutting-edge CSS feature is considered, its support across the target matrix must be checked (e.g., using Can I use...). Graceful degradation (e.g., using `@supports` queries) would be implemented if a critical feature lacks full support but this is not expected for MVP.
- **Accessibility Fallbacks:**
  - While aiming for full WCAG 2.1 AA compliance, if certain advanced ARIA patterns or JavaScript-driven accessibility enhancements are used, their behavior in slightly older (but still within "latest 2 stable") versions of assistive technologies will be considered. The use of `shadcn/ui` and standard HTML/ARIA practices should minimize such issues.

This approach ensures the application is functional and looks consistent across a modern range of browsers, prioritizing a rich interactive experience that relies on JavaScript.

## Frontend Architecture Document Review Checklist Summary

I have reviewed the generated `frontend-architecture.md` against the `frontend-architecture-checklist.txt`. Here's a summary of the review:

**I. Introduction:**

- [x] `{Project Name}` correctly filled: "Mailchimp Marketing Trends Engine".
- [x] Link to Main Architecture Document: `docs/architecture.md` (Correct).
- [x] Link to UI/UX Specification: `docs/ui-ux-spec.md` (Correct).
- [x] Link to Primary Design Files: `Final-Mailchimp-Aligned-Dashboard-Mockup.png` (Correct, as referenced in UI/UX spec).
- [x] Link to Deployed Storybook: Not applicable for MVP (Correct).

**II. Overall Frontend Philosophy & Patterns:**

- [x] Framework & Core Libraries: Clearly stated (Next.js, React, TypeScript) and aligned.
- [x] Component Architecture: Described (Feature-based, Presentational/Container, `shadcn/ui`).
- [x] State Management Strategy: High-level described (React Context/Hooks, considerations for Zustand/Jotai).
- [x] Data Flow: Explained (Unidirectional, RSC/Client Components with `Workspace`).
- [x] Styling Approach: Defined (Tailwind CSS, `shadcn/ui`, `tailwind.config.js`, Mailchimp harmony).
- [x] Key Design Patterns: Listed (Hooks, Provider, Container/Presentational, Service, Modular).
- [x] Alignment with "Definitive Tech Stack Selections": Confirmed.
- [x] Implications from overall system architecture: Considered (Monorepo context).

**III. Detailed Frontend Directory Structure:**

- [x] ASCII diagram provided and is clear.
- [x] Reflects Next.js App Router and chosen patterns.
- [x] Conventions highlighted (App Router, components, features, lib, contexts).
- [x] Notes explaining rationale are present.

**IV. Component Breakdown & Implementation Details:**

- **Component Naming & Organization:**
  - [x] Naming convention: `PascalCase` described.
  - [x] Organization explained (ui, layout, features).
- **Template for Component Specification:**
  - [x] Template is complete and well-defined.
  - [x] Includes all required fields (Purpose, Source, Visual Ref, Props, State, Structure, Events, Actions, Styling, Accessibility).
  - [x] Statement about template usage is present.
- **Foundational/Shared Components:**
  - [x] Foundational components (`GlobalHeader`, `TrendFeedPanel`, `TrendCard`, `TrendDetailsPanel`, `AiContentPanel`) specified using the template.
  - [x] Rationale is clear (derived from UI/UX spec and mockup).

**V. State Management In-Depth:**

- [x] Chosen Solution: React Context/Hooks reiterated, rationale provided.
- [x] Decision Guide for State Location: Clear distinction between Local, Context, and potential Global state.
- [x] Context API Usage: Specific contexts (`TrendsDataContext`, `SelectedTrendContext`) identified with purpose, state shape, provider logic, and consumers.
- [ ] Store Structure / Slices (for global manager): Section present but N/A for MVP, template for future use not explicitly detailed as global manager is deferred. Marked as N/A for now.
- [ ] Key Selectors (for global manager): N/A for MVP.
- [ ] Key Actions / Reducers / Thunks (for global manager): N/A for MVP.
- [x] Potential Lightweight Global State Manager: Options (Zustand, Jotai) and justification discussed.

**VI. API Interaction Layer:**

- [x] HTTP Client Setup: Detailed (`Workspace` in `frontend/lib/apiClient.ts`, base URL, headers, error shaping).
- [x] Service Definitions: Convention explained with examples in `apiClient.ts` for `getTrends`, `getTrendDetails`, `generateContentForTrend`.
- [x] Data Fetching Strategy: Detailed (RSC, Client Components with `useEffect`/`Workspace`, Next.js data cache, loading/error state management).
- [x] Global Error Handling: Described (centralized in `apiClient.ts` wrapper, specific handling in components/contexts).
- [x] Client-side Retry Logic: Explicitly stated as NOT planned for MVP.

**VII. Routing Strategy:**

- [x] Routing Library: Stated (Next.js App Router).
- [x] Route Definitions: Table provided, key MVP route `/` is listed and explained.
- [x] Route Guards / Protection: Explained as N/A for MVP but outlined for Post-MVP.

**VIII. Build, Bundling, and Deployment (Frontend Specifics - complementing main arch doc):**

- **Styling Conventions (Moved from this section in template to its own as per user prompt structure):**

  - [x] Tailwind CSS Configuration & Usage: Detailed (`tailwind.config.js`, `globals.css`, utility-first, `shadcn/ui` customization).
  - [x] Mailchimp Design Harmony: References, theme integration, component styling for Mailchimp alignment detailed.

- **Forms and User Input Handling (Moved from this section in template to its own as per user prompt structure):**

  - [x] Form Management: Detailed for MVP filters, state management via Context.
  - [x] Validation: Client-side (minimal for MVP) and server-side reliance detailed.
  - [x] Submission: Filter application (reactive) and AI content generation trigger detailed.

    *(Checklist items for Build/Bundling/Deployment from original checklist, now verifying if these are covered appropriately, even if sections were re-ordered based on user prompt)*

- [x] Build Process & Scripts: Covered by referencing Next.js standard build process and monorepo setup. `package.json` scripts in `frontend/` will contain `dev`, `build`, `start`.

- [x] Environment Variables: `NEXT_PUBLIC_API_URL` mentioned for `apiClient.ts`. `.env.local.example` in directory structure.

- [x] Code Splitting: Next.js App Router (route-based) and dynamic imports `React.lazy` or `next/dynamic` mentioned.

- [x] Tree Shaking: Handled by Next.js/Webpack.

- [x] Lazy Loading (Components, Images): `next/image` and `next/dynamic` mentioned.

- [x] Minification & Compression: Handled by Next.js build.

- [x] Target Deployment Platform: Monorepo context with local k3s (Vercel/Netlify are typical for Next.js but MVP is local). Main arch doc covers deployment.

- [x] Deployment Trigger: Via GitHub Actions (as per main arch doc).

- [x\_partial] Asset Caching Strategy: Mentioned for Next.js build outputs and RSCs. Detailed strategy usually platform-dependent but core concepts covered.

**IX. Frontend Testing Strategy:**

- [x] Link to Main Testing Strategy: Provided.
- **Component Testing:**
  - [x] Scope, Tools (Jest, RTL), Focus (rendering, interaction, basic AX with `jest-axe`), Location defined. Example provided.
- **UI Integration/Flow Testing:**
  - [x] Scope (panel interactions via Context), Tools, Focus defined. Example flow outlined.
- **End-to-End UI Testing:**
  - [x] Tools reiterated, Scope confirmed as N/A for MVP.
- **Mocking API Calls:**
  - [x] Strategy and method (`jest.mock()` for `apiClient.ts`) detailed with example.

**X. Accessibility (AX) Implementation Details:**

- [x] Semantic HTML: Emphasis and examples provided.
- [x] ARIA Implementation: Guidelines, `shadcn/ui` role, common patterns, APG reference.
- [x] Keyboard Navigation: Mandate, focus order, standard controls, custom elements.
- [x] Focus Management: Initial load, modals (post-MVP), dynamic content.
- [x] Color Contrast & Legibility: Addressed with reference to `ui-ux-spec.md` and tools.
- [x] Alt Text: Mandated.
- [x] Forms & Labels: Addressed.
- [x] Testing Tools for AX: `jest-axe`, Axe DevTools, Lighthouse, manual checks listed.
- [x] Alignment with UI/UX Spec: Confirmed.

**XI. Performance Considerations:**

- [x] Image Optimization: `next/image`, WebP, SVG, lazy loading.
- [x] Code Splitting & Lazy Loading: Reiterated with `next/dynamic`.
- [x] Minimizing Re-renders: `React.memo`, `useCallback`, `useMemo`, Context considerations.
- [x] Debouncing/Throttling: Discussed for filters if needed.
- [x] Virtualization: Discussed for long lists if needed.
- [x] Caching Strategies (Client-Side): Next.js Data Cache, Browser HTTP Caching.
- [x] Bundle Analysis: `@next/bundle-analyzer` mentioned.
- [x] Performance Monitoring Tools: DevTools, Lighthouse, WebPageTest.
- [x] Minimize Client-Side JS: Use of RSCs.

**XII. Internationalization (i18n) and Localization (l10n) Strategy:**

- [x] Marked as "Not applicable for MVP." Template structure included.

**XIII. Feature Flag Management:**

- [x] Marked as "Not applicable for MVP." Template structure included.

**XIV. Frontend Security Considerations (New Section based on user prompt structure):**

- [x] XSS Prevention: JSX escaping, `dangerouslySetInnerHTML` avoidance, CSP (general).
- [x] CSRF Protection: MVP context (stateless API) discussed, Post-MVP considerations.
- [x] Secure Token Storage: MVP (N/A), Post-MVP (`HttpOnly` cookies, in-memory).
- [x] Third-Party Script Security: MVP (minimal), Post-MVP (vetting, SRI).
- [x] Client-Side Data Validation: UX only, server-side is truth.
- [x] Clickjacking: Header-based defense (Post-MVP).
- [x] API Key Exposure: Backend proxy for Jina/Claude (correct for MVP).
- [x] Secure Communication (HTTPS): Mandated for non-local, local context explained.
- [x] Dependency Vulnerabilities: `pnpm audit`, CI integration.

**XV. Browser Support and Progressive Enhancement (New Section based on user prompt structure):**

- [x] Target Browsers: Defined (latest 2 stable of Chrome, Firefox, Safari, Edge).
- [x] Polyfill Strategy: Next.js handles most.
- [x] JavaScript Requirement: Required for MVP. No-JS experience not a goal.
- [x] CSS Compatibility: Autoprefixer, modern CSS.
- [x] Accessibility Fallbacks: General consideration.

**XVI. Change Log (from original template):**

- [x] Table present and initialized with the creation of this document.
- [x] Process for updates implied by versioning.

**Final Review Sign-off:**

- [x] Placeholders filled.
- [x] Document reviewed for clarity, consistency, and completeness.
- [x] Relies on stable input documents (`architecture.md`, `ui-ux-spec.md`, `prd.md`).
- [x] The document appears ready to be shared.

**Summary of Checklist Review:**
All relevant sections of the checklist have been satisfied in the `frontend-architecture.md` document. Sections like global state management details (slices, selectors, thunks for a global manager like Zustand/Jotai), full E2E UI testing, i18n, and feature flags were marked as not applicable or deferred for MVP, which is consistent with the project's scope. The document structure was adapted to better fit the user's prompt (e.g., dedicated sections for Styling, Forms, Security, Browser Support). The content is comprehensive and addresses all tasks outlined in the initial prompt. No significant deficiencies were identified that require immediate attention for the MVP scope.

The `frontend-architecture.md` document is now complete and validated.

[architecture-doc]: docs/architecture.md
[ui-ux-spec]: docs/ui-ux-spec.md
[mock-up-image]: docs/Final-Mailchimp-Aligned-Dashboard-Mockup.png
[Media-Kit-Mailchimp]: docs/515-Media-Mailchimp-User-Guide-REV2.pdf
