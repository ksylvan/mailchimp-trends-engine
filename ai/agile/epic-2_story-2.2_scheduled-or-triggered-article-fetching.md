# Story 2.2: Scheduled or Triggered Article Fetching

## Status: Completed

## Story

- As a Backend Developer
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

- [x] Task 1: Integrate Scheduling Library (AC: #1)
  - [x] Add `APScheduler` (or a similar lightweight scheduling library like `schedule`) to `backend/pyproject.toml` dependencies and update the environment using `uv sync`.
  - [x] In `backend/app/data_ingestion/scheduler.py` and `backend/app/server.py` (lifespan event):
    - [x] Initialize the scheduler instance.
    - [x] Ensure the scheduler starts with FastAPI and shuts down gracefully.
- [x] Task 2: Define the Article Fetching Job (AC: #2, #3, #6)
  - [x] Create an `async` function (`perform_scheduled_article_fetch` in `scheduler.py`) that will be executed.
  - [x] Inside this function:
    - [x] Retrieve the list of `NEWS_SOURCES` from `core.config.settings`.
    - [x] Log the start of the fetch cycle.
    - [x] Iterate through each URL in `NEWS_SOURCES`.
      - [x] Call `jina_ai_service.fetch_article_content(url)`.
      - [x] If content is fetched, pass it to a placeholder function for storage (`process_fetched_content`). Logged content length.
      - [x] Implement a small delay (`await asyncio.sleep(settings.JINA_FETCH_DELAY_SECONDS)`) after each call.
    - [x] Log the end of the fetch cycle.
- [x] Task 3: Configure Job Scheduling or Manual Trigger (AC: #4)
  - [x] **Option A (Scheduled):**
    - [ ] Configure the scheduler to run `perform_scheduled_article_fetch` at a defined interval (e.g., every 2 hours). Make this interval configurable via an environment variable (e.g., `Workspace_INTERVAL_MINUTES`). (Deferred for now, manual trigger implemented)
  - [x] **Option B (Manual Trigger for MVP Demo):**
    - [x] Create a new API endpoint in `backend/app/api/v1/routers/data_ingestion.py` (`/trigger-fetch`) that, when called, manually executes `perform_scheduled_article_fetch`.
    - [x] Endpoint is unsecured for local MVP.
  - [x] *Decision for MVP: Implement Option B (Manual Trigger API) for easier demo control, but design `perform_scheduled_article_fetch` so it could be easily scheduled later.* (Implemented)
- [x] Task 4: Enhance Logging (AC: #5)
  - [x] `perform_scheduled_article_fetch` logs overall start/completion and any errors during iteration.
  - [x] Individual error logging within `fetch_article_content` (from Story 2.1) remains.
- [x] Task 5: Unit/Integration Testing for Scheduler (Conceptual)
  - [x] *Testing actual schedulers can be complex. For this story, focus on ensuring the `perform_scheduled_article_fetch` function works correctly when called directly.* (Focused on this)
  - [x] Create tests for `perform_scheduled_article_fetch` in `tests/unit/data_ingestion/test_scheduler.py`:
    - [x] Mock `jina_ai_service.fetch_article_content`.
    - [x] Mock `core.config.settings.NEWS_SOURCES` and `JINA_FETCH_DELAY_SECONDS`.
    - [x] Verify it iterates through URLs, calls the fetch function for each, and implements delays.
    - [x] Verify logging.
  - [ ] Manually verify the trigger API endpoint (if implemented) successfully initiates the fetch process. (Can be done post-completion if needed for full verification)

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

### Change Log

- 2025-05-17 - Kayvan Sylvan - Initial draft
