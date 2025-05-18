# Mailchimp Marketing Trends Engine UI/UX Specification

## Introduction

The purpose of this document is to define the user experience goals, information architecture, user flows, and visual design specifications for the Mailchimp Marketing Trends Engine's user interface. It aims to ensure a user-friendly, intuitive dashboard that aligns seamlessly with Mailchimp's established aesthetics and user experience principles, as detailed in the project's Product Requirements Document (PRD) and inspired by the Mailchimp User Guide and the "Final-Mailchimp-Aligned-Dashboard-Mockup.png".

- **Link to Primary Design Files:** Not applicable (No Figma/Sketch designs will be created for this MVP). The conceptual descriptions within this document, along with the "Final-Mailchimp-Aligned-Dashboard-Mockup.png" (referenced in the Wireframes & Mockups section), serve as the primary visual and structural reference.
- **Link to Mailchimp User Guide (for UI/UX Inspiration):** `515-Media-Mailchimp-User-Guide-REV2.pdf` (User Provided)
- **Link to Deployed Storybook / Design System:** Not applicable for MVP.

## Overall UX Goals & Principles

- **Target User Personas:**
  - The Mailchimp user, typically a business owner or their designated marketing department/personnel, who is looking for ways to enhance their marketing campaigns with timely and relevant trend data and content inspiration.
  - Consideration: The UI should be intuitive for users with varying levels of technical savvy, from small business owners to experienced marketers.
- **Usability Goals:**
  - Intuitive discovery of marketing trends.
  - Clear and scannable presentation of trend data.
  - Efficient generation and retrieval of AI-powered content ideas.
  - Seamless and familiar experience for existing Mailchimp users.
  - Discoverability of Features: Users should easily find and understand the capabilities of the Trends Engine.
  - Confidence & Trust: The data presented should feel reliable, and the AI suggestions useful, building user confidence in the tool.
- **Design Principles:**
  - **Mailchimp Harmony:** The UI must feel like a natural extension of the Mailchimp platform, adhering to its established design language and interaction patterns.
  - **Clarity & Simplicity:** Prioritize ease of understanding and use, avoiding unnecessary complexity. "Simpler is better."
  - **Actionability:** Enable users to quickly move from insight (viewing trends) to action (generating content ideas).
  - **Efficiency:** Streamline workflows for discovering trends and creating content.

## Information Architecture (IA)

The Mailchimp Marketing Trends Engine is designed as a **Single-Page Application (SPA)**, presenting users with a unified dashboard experience. The IA focuses on the key functional areas within this single view rather than a collection of separate, navigable pages.

- **Overall Dashboard Title/Context:** Marketing Trends

- **Screen Inventory (Functional Areas within the SPA):**

    1. **Global Header:** A consistent top bar styled to match Mailchimp's branding (e.g., logo, potential mock user/account elements for visual consistency). This provides context and brand alignment.
    2. **Trend Feed & Filters Panel:**
          - **Purpose:** Allows users to discover and browse current marketing trends.
          - **Content:** Displays a list/grid of trend cards (showing trend name, date, sentiment, score). Features controls for filtering trends (e.g., by category, sentiment).
    3. **Trend Details & Visualization Panel:**
          - **Purpose:** Provides an in-depth view of a specific trend selected from the "Trend Feed & Filters Panel."
          - **Content:** Shows detailed information about the selected trend and includes a time-series chart illustrating its performance metrics (e.g., mention frequency/score over time).
    4. **AI Content Generation Panel:**
          - **Purpose:** Enables users to generate marketing content ideas based on the selected trend.
          - **Content:** Displays AI-generated content (e.g., email subject lines, body copy, campaign themes) and includes a trigger for content generation and copy-to-clipboard functionality.

- **Navigation Structure (Interaction-Driven):**

  - Navigation within the "Marketing Trends" dashboard is primarily driven by user interactions rather than traditional page links.
  - **Filtering Trends:** Applying filters in the "Trend Feed & Filters Panel" dynamically updates the list of trends shown in that same panel.
  - **Selecting a Trend:** Clicking a trend in the "Trend Feed & Filters Panel" populates the "Trend Details & Visualization Panel" with the selected trend's data and sets the context for the "AI Content Generation Panel."
  - **Generating Content:** Activating the generation feature in the "AI Content Generation Panel" (usually after a trend is selected) processes the request and displays the results within that panel.
  - The conceptual relationship and flow between these panels can be visualized as:

    ```mermaid
    graph TD
        subgraph "Marketing Trends"
            Header["Global Header (Mailchimp Style)"]

            Panel1["Trend Feed & Filters Panel"]
            Panel2["Trend Details & Visualization Panel"]
            Panel3["AI Content Generation Panel"]

            Panel1 -- "User selects a trend" --> Panel2
            Panel2 -- "Provides context for" --> Panel3
            Panel3 -- "User clicks 'Generate Content'" --> Panel3_Content{Generated Content Displayed}

            Header --> Panel1
            Header --> Panel2
            Header --> Panel3
        end
    ```

- **Proposed Spatial Layout (Conceptual):**

  - A multi-column layout is favored for desktop views to keep information accessible:
    - **Left Column:** "Trend Feed & Filters Panel."
    - **Main/Center Column:** "Trend Details & Visualization Panel."
    - **Right Column:** "AI Content Generation Panel."
  - This layout aims to provide a clear overview and easy transitions between discovering, analyzing, and acting on trends. This is visually represented in "Final-Mailchimp-Aligned-Dashboard-Mockup.png".

## User Flows

### User Flow 1: Discovering and Exploring Marketing Trends

- **Goal:** The user wants to identify relevant marketing trends, understand their significance, and select one for further analysis or content generation.
- **Actor:** Mailchimp User (Business Owner, Marketer)
- **Preconditions:** The user has accessed the "Marketing Trends" dashboard. Trend data has been ingested and processed by the backend.
- **Steps / Diagram:**

    ```mermaid
    graph TD
        A[Start: User lands on &quot;Marketing Trends&quot; dashboard] --> B{Trend Feed & Filters Panel is populated with initial list of trends};
        B --> C{"User views the list of trends (trend name, score, sentiment, date)"};
        C --> D{"User has an option to apply filters (e.g., by category, sentiment)"};
        D -- "Applies Filters" --> E[Trend Feed is updated based on filters];
        D -- "No Filters Applied or Filters Cleared" --> C;
        E --> C;
        C --> F{User identifies an interesting trend and clicks on it};
        F --> G[Trend Details & Visualization Panel updates to show selected trend's details and chart];
        G --> H[Context for AI Content Generation Panel is set to the selected trend];
        H --> End1[End: User has explored a trend and is ready to generate content or explore another trend];
    ```

- **Success Condition:** The user can successfully view trends, filter them, and select a specific trend to see its detailed information and visualization.
- **Error States/Edge Cases & Empty States (Conceptual):**
  - **No trends available:** The Trend Feed panel should display a clear, Mailchimp-aligned friendly message (e.g., "No marketing trends identified yet. Please check back later." or "Data is currently being updated.").
  - **Filter results in no trends:** A message like "No trends match your current filters. Try adjusting your selections."
  - **Failed to load trend details:** The Trend Details panel should show an appropriate error message (e.g., "Unable to load details for this trend. Please try again.") with a potential retry option.
  - **Loading States:** Subtle loading indicators (e.g., spinner or shimmer effect) should be used within panels during data fetching or processing.

### User Flow 2: Generating AI-Powered Marketing Content Ideas

- **Goal:** The user wants to get actionable marketing content suggestions (email subjects, body copy, themes) for a selected marketing trend.
- **Actor:** Mailchimp User (Business Owner, Marketer)
- **Preconditions:**
  - The user has selected a trend.
  - The LLM integration is functional.
- **Steps / Diagram (Simplified for clarity, refer to detailed text below):**

    ```mermaid
    graph TD
        A["Start: Trend Selected"] --> B["User Interacts with AI Panel"];
        B --> C["Sees 'Generate' Button"];
        C -- "Clicks Button" --> D["System Calls LLM"];
        D --> E["Loading State Shown"];
        E --> F["LLM Returns Suggestions"];
        F -- "Success" --> G["Content Displayed"];
        G --> H["'Copy' Option Available"];
        H -- "User Clicks 'Copy'" --> I["Feedback: Copied!"];
        H --> End2["End: User Has Ideas"];
        F -- "Error" --> J["Error Message Shown"];
        J --> C;
    ```

- **Detailed Steps (Text):**
    1. Start: User has a trend selected in the "Trend Details & Visualization Panel."
    2. User interacts with the "AI Content Generation Panel."
    3. User sees a "Generate Content Ideas" button.
    4. User clicks the button; system sends trend data to LLM.
    5. AI Content Generation Panel shows a loading state.
    6. LLM processes and returns suggestions.
    7. (Success): Generated content (email subjects, body copy, themes) is displayed.
    8. Each piece of content has a "Copy to Clipboard" option.
    9. User clicks "Copy"; content is copied with feedback.
    10. End: User has content ideas.
    11. (Error from LLM): Panel displays a user-friendly error message (e.g., "Could not generate content. Please try again.") with a possible retry.
- **Success Condition:** The user successfully receives relevant marketing content ideas and can copy them.
- **Error States/Edge Cases & Empty States (Conceptual):**
  - **LLM API Issues:** User-friendly "Feature unavailable," "Configuration error," or "Could not generate suggestions, please try again."
  - **No useful content from LLM:** Panel indicates no suggestions could be generated for the specific trend.
  - **Copy to clipboard failure:** Graceful fallback or message.
  - **Loading States:** Clear indication within the AI Content Generation Panel while LLM is processing.

## Wireframes & Mockups (Conceptual Descriptions)

This section provides detailed textual descriptions of the key views and panels for the Mailchimp Marketing Trends Engine, guided by the **"Final-Mailchimp-Aligned-Dashboard-Mockup.png"** image and the user-provided "Changes Made to Align with Mailchimp Design Elements" list. These descriptions are intended to guide development and can be used as input for AI-driven mockup generation tools. All visual styling, component appearance, and interaction patterns should strive for "Mailchimp Harmony," referencing the Mailchimp User Guide and the live Mailchimp application as primary sources of inspiration.

- **Link to Key Visual Mockup:** `Final-Mailchimp-Aligned-Dashboard-Mockup.png` (User Provided).
- **Link to Mailchimp User Guide (for UI/UX Inspiration):** `515-Media-Mailchimp-User-Guide-REV2.pdf` (User Provided).
- **Core Styling Rationale:** Derived from user-provided "Changes Made to Align with Mailchimp Design Elements," focusing on specific Mailchimp colors (Cavendish Yellow, Peppercorn, etc.), typography (Helvetica Neue), and UI element treatments.

-----

### 1\. Main Dashboard View: Overall Layout & Structure

(As detailed in previous interactions, describing the Global Header and the three-column layout for Left: "Trend Feed & Filters Panel," Center: "Trend Details & Visualization Panel," Right: "AI Content Generation Panel," and basic responsiveness notes. All details aim to match the "Final-Mailchimp-Aligned-Dashboard-Mockup.png".)

-----

### 2\. Trend Feed & Filters Panel (Left Column)

(As detailed in previous interactions, describing the "Current Trends" title, filter controls section with Category dropdown and Sentiment toggle, and the Trend List section with Trend Card appearance, hover/selected states, and empty state handling. All details aim to match the "Final-Mailchimp-Aligned-Dashboard-Mockup.png".)

-----

### 3\. Trend Details & Visualization Panel (Center Column)

(As detailed in previous interactions, describing the initial state, selected trend display with header/title, key metrics, and the time-series chart visualization section. All details aim to match the "Final-Mailchimp-Aligned-Dashboard-Mockup.png".)

-----

### 4\. AI Content Generation Panel (Right Column)

(As detailed in previous interactions, describing the header/title, initial state/prompt, "Generate Ideas" button, loading state, and the display of generated content sections with copy-to-clipboard functionality. All details aim to match the "Final-Mailchimp-Aligned-Dashboard-Mockup.png".)

-----

## Component Library / Design System Reference

- **Core Technologies:** The project will utilize **shadcn/ui** as a foundation for unstyled, accessible components, with **Tailwind CSS** employed for all styling to achieve "Mailchimp Harmony."
- **Visual & Styling Guide:**
  - The primary visual reference is the **"Final-Mailchimp-Aligned-Dashboard-Mockup.png"**.
  - The detailed styling rules are derived from the user-provided "Changes Made to Align with Mailchimp Design Elements" list, which specifies Mailchimp's color palette (Cavendish Yellow, Peppercorn, etc.), typography (Helvetica Neue), and UI element treatments (buttons, cards, forms) based on the Mailchimp User Guide.
- **Tailwind CSS Configuration:**
  - `tailwind.config.js`: Will be extended to include the Mailchimp-specific color palette and any project-specific font configurations.
  - `globals.css`: Will define base typographic styles (e.g., default body font to Helvetica Neue) and global background colors.
- **Iconography:**
  - **Lucide Icons** (or a similar comprehensive SVG icon library compatible with Tailwind CSS styling) is the preferred choice. Icons should be selected and styled to match the visual weight and simplicity observed in Mailchimp's UI and the "Final-Mailchimp-Aligned-Dashboard-Mockup.png."
- **Foundational Components (Conceptual List - to be built using shadcn/ui & styled with Tailwind):**
  - **`McButton`**: Based on `shadcn/ui Button`. Variants for primary (Peppercorn background, white text), secondary (e.g., filter toggles), and icon-only (e.g., copy buttons). Styling to match Mailchimp CTAs and interactive elements.
  - **`McTrendCard`**: Based on `shadcn/ui Card`. Styling to match the trend card appearance in the mockup (padding, border, selected state with yellow accent, internal layout).
  - **`McFilterDropdown`**: Based on `shadcn/ui Select`. Styling to align with Mailchimp form input styles (borders, focus states).
  - **`McSentimentToggle`**: Based on `shadcn/ui Toggle Group` or custom-styled `McButton`s. Visuals to clearly indicate selection and align with overall filter design.
  - **`McPanel`**: Based on `shadcn/ui Card` or styled `div`. Used for the main columnar layout panels, with specified background, shadow, and padding.
  - **`McChartWrapper`**: A custom wrapper to encapsulate Chart.js instances, ensuring consistent styling (Mailchimp colors, minimal axis/legend presentation) as per the mockup.
- **Development Approach:** Developers will use `shadcn/ui` components as building blocks and apply Tailwind CSS utility classes directly or create minimal custom component abstractions where necessary to achieve the precise look and feel of the "Final-Mailchimp-Aligned-Dashboard-Mockup.png" and adhere to Mailchimp's design language.

## Branding & Style Guide Reference

- **Primary Source:** The "Final-Mailchimp-Aligned-Dashboard-Mockup.png" and the accompanying user-provided "Changes Made to Align with Mailchimp Design Elements" list serve as the primary, detailed style guide for this project. The Mailchimp User Guide (`515-Media-Mailchimp-User-Guide-REV2.pdf`) is the overarching inspiration.
- **Color Palette:**
  - **Cavendish Yellow (\#FFE01B):** Primary accent (chart lines, selected borders, hover effects).
  - **Peppercorn (\#2E2E2E):** Dark accents (header background, buttons, text accents).
  - **Light Grey (\#F5F6F5):** Page background.
  - **White (\#FFFFFF):** Panel backgrounds, card backgrounds.
  - **Subtle Yellow Tint (\#FFF8D1):** Hover states.
  - **Border Grey (\#E0E0E0):** Card borders, form input borders.
- **Typography:**
  - **Font Family:** Helvetica Neue (fallback to Arial, sans-serif).
  - **Weights & Sizes (examples, refer to mockup & User Guide):**
    - Panel Titles: Bold, approx. 18px.
    - Body Text / Primary Content: Regular, approx. 14px.
    - Secondary Info (e.g., dates on cards): Regular/Light, approx. 12px.
- **Iconography:**
  - **Library:** Lucide Icons (preferred).
  - **Style:** Simple, clean, line-art style; styled with Tailwind CSS.
  - **Usage:** As per "Final-Mailchimp-Aligned-Dashboard-Mockup.png" (sentiment indicators, copy-to-clipboard actions, help icons, user avatar placeholders).
- **Spacing & Grid:**
  - **General Principle:** Clean, uncluttered, with adequate white space, derived from "Final-Mailchimp-Aligned-Dashboard-Mockup.png" and Mailchimp User Guide examples.
  - **Grid System:** 3-column responsive layout for desktop, using Tailwind's flexbox and grid utilities.

## Accessibility (AX) Requirements

- **Target Compliance:** WCAG 2.1 Level AA.
- **Specific Requirements:**
  - **Semantic HTML:** Utilize HTML elements according to their intended meaning.
  - **Keyboard Navigation:** All interactive elements must be focusable and operable via keyboard; focus order must be logical. Standard keyboard interactions for common elements.
  - **ARIA Landmarks:** Use for page regions (e.g., `<header>`, `<main>`).
  - **ARIA Attributes:** For custom components (trend cards, filter controls, chart, copy buttons) including accessible names and states (e.g., `aria-current`, `aria-checked`, `aria-label`, `aria-live="polite"` for feedback).
  - **Color Contrast:** Meet WCAG AA ratios (4.5:1 for normal text, 3:1 for large text/UI components), as guided by the defined color palette.
  - **Legible Fonts:** As per typography guidelines.
  - **Responsive Design:** Ensure usability across screen sizes.
  - **Focus Management (MVP):** Standard browser focus behavior. No complex focus trapping unless modals are introduced.
  - **Alternative Text:** For all informational images (e.g., Mailchimp logo) and icons.
  - **Chart Accessibility (MVP):** Provide an accessible name (`aria-label`). Key data points also available textually in the "Key Metrics" section. (Post-MVP: consider a data table fallback).

## Responsiveness

- **Breakpoints (Tailwind CSS Defaults):**
  - `sm`: `640px`
  - `md`: `768px`
  - `lg`: `1024px`
  - `xl`: `1280px`
  - `2xl`: `1536px`
- **Adaptation Strategy:**
  - **Mobile & Tablet (up to `lg`, `<1024px`):** Single-column vertical stack for the three main panels ("Trend Feed & Filters," "Trend Details & Visualization," "AI Content Generation"). Filters might collapse to save space. Charts resize. Each panel takes full viewport width (minus standard padding).
  - **Desktop (`lg` and above, `>=1024px`):** Three-column layout as depicted in "Final-Mailchimp-Aligned-Dashboard-Mockup.png".
  - **General Considerations:** Ensure adequate touch target sizes and maintain readability across all screen sizes.

## Change Log

| Change                                      | Date         | Version | Description                                                                                                | Author                                           |
| :------------------------------------------ | :----------- | :------ | :--------------------------------------------------------------------------------------------------------- | :----------------------------------------------- |
| Initial Draft populated based on user input | May 17, 2025 | 1.0     | Populated all sections through collaborative discussion, including IA, User Flows, Mockup references, etc. | 4-design-architect (AI Design Architect)         |
