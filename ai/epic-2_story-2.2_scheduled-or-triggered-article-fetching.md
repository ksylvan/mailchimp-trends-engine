# Story 2.2: Scheduled or Triggered Article Fetching

## Status: Draft

## Story

- As a Backend Developer Agent
- I want to implement a mechanism for periodically fetching new articles from the configured news sources using the Jina AI Reader service
- so that the system continuously ingests fresh content for trend analysis.

## Acceptance Criteria (ACs)

1. A scheduling mechanism (e.g., using `APScheduler` or a similar library) is integrated into the backend application.
2. The scheduler is configured to periodically trigger a task that iterates through the configured list of news URLs (from `core/config.py`).
3. For each URL, the `Workspace_article_content` function (from Story 2.1's `jina_ai_service.py`) is called to get the article content.
4. (Simplified for MVP) The scheduler can be configured with a reasonable interval (e.g., every 1-4 hours, or a manually triggered API endpoint for MVP demo purposes is also acceptable).
5. Appropriate logging is implemented for the start and end of a fetch cycle, and for any errors encountered while fetching individual articles (building on Story 2.1 error logging).
6. The fetching process respects Jina AI Reader's rate limits (20 RPM for keyless) by incorporating a small delay (e.g., 3-5 seconds) between calls to `Workspace_article_content` if multiple URLs are processed in a single cycle.

## Tasks / Subtasks

- [ ] Task 1: Integrate Scheduling Library (AC: #1)
  - [ ] Add `APScheduler` (or a similar lightweight scheduling library like `schedule`) to `backend/pyproject.toml` dependencies and update the environment using `uv sync`.
  - [ ] In `backend/src/mailchimp_trends/main.py` or a dedicated scheduling module (e.g., `data_ingestion/scheduler.py`):
    - [ ] Initialize the scheduler instance when the FastAPI application starts.
    - [ ] Ensure the scheduler shuts down gracefully when the FastAPI application stops.
- [ ] Task 2: Define the Article Fetching Job (AC: #2, #3, #6)
  - [ ] Create an `async` function (e.g., `perform_scheduled_article_fetch`) that will be executed by the scheduler.
  - [ ] Inside this function:
    - [ ] Retrieve the list of `NEWS_SOURCES` from `core.config.settings`.
    - [ ] Log the start of the fetch cycle.
    - [ ] Iterate through each URL in `NEWS_SOURCES`.
      - [ ] Call `jina_ai_service.fetch_article_content(url)`.
      - [ ] If content is fetched, pass it to a placeholder function for storage (actual storage is Story 2.3). For now, just log the fetched content's length or a snippet.
      - [ ] Implement a small delay (e.g., `await asyncio.sleep(4)`) after each call to respect Jina's rate limit.
    - [ ] Log the end of the fetch cycle.
- [ ] Task 3: Configure Job Scheduling or Manual Trigger (AC: #4)
  - [ ] **Option A (Scheduled):**
    - [ ] Configure the scheduler to run `perform_scheduled_article_fetch` at a defined interval (e.g., every 2 hours). Make this interval configurable via an environment variable (e.g., `Workspace_INTERVAL_MINUTES`).
  - [ ] **Option B (Manual Trigger for MVP Demo):**
    - [ ] Create a new API endpoint in a router (e.g., `api/v1/admin/trigger-fetch`) that, when called, manually executes `perform_scheduled_article_fetch`. This is useful for demos.
    - [ ] Secure this endpoint if necessary (though for local MVP, basic access is fine).
  - [ ] *Decision for MVP: Implement Option B (Manual Trigger API) for easier demo control, but design `perform_scheduled_article_fetch` so it could be easily scheduled later.*
- [ ] Task 4: Enhance Logging (AC: #5)
  - [ ] Ensure `perform_scheduled_article_fetch` logs overall start/completion and any errors during iteration (e.g., if `Workspace_article_content` returns None).
  - [ ] The individual error logging within `Workspace_article_content` (from Story 2.1) should remain.
- [ ] Task 5: Unit/Integration Testing for Scheduler (Conceptual)
  - [ ] *Testing actual schedulers can be complex. For this story, focus on ensuring the `perform_scheduled_article_fetch` function works correctly when called directly.*
  - [ ] Create tests for `perform_scheduled_article_fetch`:
    - [ ] Mock `jina_ai_service.fetch_article_content`.
    - [ ] Mock `core.config.settings.NEWS_SOURCES`.
    - [ ] Verify it iterates through URLs, calls the fetch function for each, and implements delays.
    - [ ] Verify logging.
  - [ ] Manually verify the trigger API endpoint (if implemented) successfully initiates the fetch process.

## Dev Technical Guidance

- **Scheduler Choice:** `APScheduler` is robust. For extreme simplicity in an MVP, the `schedule` library is also an option if complex scheduling features (like persistence, clustering) are not needed. Given FastAPI's async nature, ensure the chosen scheduler integrates well with `asyncio`.
- **Async Delays:** Use `await asyncio.sleep(seconds)` for delays within the async fetch job. A 3-5 second delay should keep a small list of sources under Jina's 20 RPM limit (e.g., 5 sources * 4s/source = 20s cycle, well within a minute).
- **Manual Trigger API Endpoint:** If creating this, it could be a simple `POST` request to an endpoint like `/api/v1/data/ingest/trigger` which then calls `await perform_scheduled_article_fetch()`.
- **Configuration:**
  - `Workspace_INTERVAL_MINUTES`: If using scheduled approach, add to `core/config.py` and `.env.example`.
  - `JINA_FETCH_DELAY_SECONDS`: Add to `core/config.py` (e.g., default to 4 seconds) and use this in `perform_scheduled_article_fetch`.
- **Logging:** Ensure logs clearly indicate which URL is being fetched and whether it was successful or resulted in an error.
- **Placeholder for Storage:** Since Story 2.3 handles actual storage, the `perform_scheduled_article_fetch` function, after getting content, can just log it or call a dummy "process_fetched_content(url, content)" function for now.

## Story Progress Notes

### Completion Notes List

{Any notes about implementation choices, difficulties, or follow-up needed}

### Change Log

2025-05-17 - Kayvan Sylvan - {Description of Change, e.g., "Story Drafted"}
