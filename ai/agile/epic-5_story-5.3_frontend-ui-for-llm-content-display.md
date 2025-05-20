# Story 5.3: Frontend UI for LLM Content Display & Copy-Paste

## Status: Draft

## Story

- As a Frontend Developer
- I want to implement the UI in the "AI Content Generation Panel" for triggering content generation, displaying the LLM-generated ideas (email subjects, body copy, themes), and providing copy-to-clipboard functionality
- so that users can easily interact with the AI content generation feature and utilize its outputs, with styling aligned to Mailchimp.

## Acceptance Criteria (ACs)

1. The "AI Content Generation Panel" (e.g., `AiContentPanel.tsx`) displays a button (e.g., "Generate Ideas with AI" or "Draft with Claude"). This button is disabled if no trend is selected.
2. Clicking the "Generate Ideas" button triggers a call to the backend API endpoint (`POST /api/v1/trends/{trend_id}/generate-content-ideas`) using `apiClient.ts`.
3. A loading state (e.g., button disabled with "Generating..." text, or a spinner within the panel) is displayed while the API call is in progress.
4. If the API call is successful, the generated content (email subject lines, body copy, campaign themes) is displayed in distinct, clearly labeled sections within the panel.
5. Each piece of generated content (e.g., each subject line, the body copy paragraph, each campaign theme) has an associated "Copy to Clipboard" button/icon.
6. Clicking a "Copy to Clipboard" button copies the corresponding text to the user's clipboard and provides brief visual feedback (e.g., icon changes to a checkmark, "Copied!" tooltip/toast).
7. If the API call fails, a user-friendly error message is displayed within the panel.
8. The UI elements (button, content display areas, copy buttons) are styled to align with Mailchimp's aesthetics (referencing `ui-ux-spec.md` and `Final-Mailchimp-Aligned-Dashboard-Mockup.png`).
9. All interactive elements are keyboard accessible.

## Tasks / Subtasks

- [ ] Task 1: Implement `AiContentPanel` Structure and Button (AC: #1, #8)
  - [ ] Create or refine `frontend/components/layout/AiContentPanel.tsx`.
  - [ ] It should receive `selectedTrendId` and `selectedTrendName` as props (likely from `SelectedTrendContext` or parent page).
  - [ ] Add a primary CTA button (e.g., `shadcn/ui Button` styled like Peppercorn Mailchimp button) labeled "Generate Ideas" or "Draft with Claude".
  - [ ] Button is `disabled` if `selectedTrendId` is null or if `isLoading` state is true.
  - [ ] Display `selectedTrendName` if a trend is selected. If no trend is selected, show a message like "Select a trend to generate content ideas."
- [ ] Task 2: Implement API Call and Loading/Error States (AC: #2, #3, #7)
  - [ ] In `AiContentPanel.tsx`, add state variables: `generatedContent: GeneratedContentIdeasSchema | null`, `isLoading: boolean`, `error: string | null`.
  - [ ] Implement `handleGenerateContent` async function:
    - [ ] Set `isLoading` to true, `error` to null.
    - [ ] Call `apiClient.generateContentForTrend(selectedTrendId)`.
    - [ ] On success: update `generatedContent` state with response, set `isLoading` to false.
    - [ ] On error: set `error` state with a user-friendly message, set `isLoading` to false.
  - [ ] Wire `handleGenerateContent` to the "Generate Ideas" button's `onClick`.
  - [ ] Conditionally render loading indicators (e.g., change button text to "Generating...", show a spinner) and error messages.
- [ ] Task 3: Display Generated Content (AC: #4, #8)
  - [ ] When `generatedContent` state is populated and not null:
    - [ ] Create clearly labeled sections for "Email Subject Lines", "Email Body Copy", and "Campaign Themes".
    - [ ] For subject lines and themes (lists): iterate and display each item.
    - [ ] For body copy (string): display the paragraph.
    - [ ] Style these sections for readability, aligning with Mailchimp aesthetics (e.g., using `shadcn/ui Card` sub-components or styled divs).
- [ ] Task 4: Implement "Copy to Clipboard" Functionality (AC: #5, #6)
  - [ ] Create a reusable `CopyButton.tsx` component (e.g., in `components/ui/`).
    - [ ] Props: `textToCopy: string`.
    - [ ] Internal state: `isCopied: boolean`.
    - [ ] On click, use `navigator.clipboard.writeText(textToCopy)`. Set `isCopied` to true, then reset after a short delay (e.g., 2 seconds).
    - [ ] Display a "Copy" icon (e.g., `Copy` from Lucide Icons). If `isCopied` is true, display a "Check" icon and/or change tooltip/text briefly.
  - [ ] Integrate `CopyButton` next to each generated subject line, the body copy block, and each campaign theme.
- [ ] Task 5: Ensure Keyboard Accessibility (AC: #9)
  - [ ] "Generate Ideas" button must be focusable and activatable with Enter/Space.
  - [ ] `CopyButton` instances must be focusable and activatable.
  - [ ] If content sections are scrollable, ensure they are keyboard scrollable.
- [ ] Task 6: Unit/Integration Tests for `AiContentPanel` and `CopyButton`
  - [ ] Test `CopyButton`:
    - [ ] Mock `navigator.clipboard.writeText`.
    - [ ] Verify it's called with correct text on click.
    - [ ] Verify `isCopied` state change and visual feedback (if testable).
  - [ ] Test `AiContentPanel`:
    - [ ] Mock `SelectedTrendContext` (or props for `selectedTrendId`).
    - [ ] Mock `apiClient.generateContentForTrend`.
    - [ ] Test initial state (button disabled if no trend).
    - [ ] Test clicking "Generate Ideas": verify API call, loading state, then display of mock generated content on success, or error message on failure.
    - [ ] Verify `CopyButton`s are rendered with generated content.
  - [ ] Include `jest-axe` accessibility checks for both components.

## Dev Technical Guidance

- **State Management:** `AiContentPanel` will likely manage its own state for `generatedContent`, `isLoading`, and `error`. It will consume `selectedTrendId` (and potentially `selectedTrendName`) from a context like `SelectedTrendContext` or props.
- **`apiClient.ts`:** Ensure `generateContentForTrend(trendId)` function is implemented in `apiClient.ts` to call `POST /api/v1/trends/{trend_id}/generate-content-ideas`.
- **Styling:**
  - Refer to `Final-Mailchimp-Aligned-Dashboard-Mockup.png` for the "Get Content Ideas" panel layout.
  - Button styling should be consistent with Mailchimp's primary CTAs (Peppercorn background).
  - Generated content should be presented clearly. Use `shadcn/ui Card` or similar for structuring if it fits the aesthetic.
- **Copy to Clipboard:** `navigator.clipboard` is a modern asynchronous API. Ensure error handling for `writeText` if necessary, though it's generally reliable in secure contexts (HTTPS or localhost).
- **Lucide Icons:** Use for "Copy" (`Copy`), "Check" (`Check`), and potentially loading spinners (`Loader2`).
- **User Feedback for Copy:** A brief change in the icon (Copy -> Check) or a small, temporary "Copied!" text/tooltip next to the button is good UX. `shadcn/ui Tooltip` can be used.

## Story Progress Notes

### Completion Notes List

### Change Log

- 2025-05-17 - Kayvan Sylvan - Initial draft
