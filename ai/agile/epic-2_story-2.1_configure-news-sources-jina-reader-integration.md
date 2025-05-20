# Story 2.1: Configure News Sources & Basic Jina AI Reader Integration

## Status: Complete

## Story

- As a Backend Developer
- I want to configure a list of news sources and integrate the Jina AI Reader API (`r.jina.ai/URL`)
- so that the system can fetch and extract primary textual content from these online news articles for subsequent processing.

## Acceptance Criteria (ACs)

1. A configurable list of 3-5 diverse general news website URLs (e.g., main news homepages or specific sections that frequently update) is defined in the backend application's configuration.
2. A backend module (e.g., within `data_ingestion/`) is created to handle interaction with the Jina AI Reader API.
3. This module includes a function that takes a URL as input and makes a GET request to `https://r.jina.ai/{URL_to_read}`.
4. The function correctly parses the response from Jina AI Reader to extract the primary textual content (plain text or Markdown).
5. Basic error handling is implemented for the Jina AI Reader API call (e.g., network errors, non-200 status codes), and errors are logged.
6. A unit test is implemented for the Jina AI Reader interaction function, mocking the `httpx` call, to verify:
    - [x] Correct URL construction for Jina AI.
    - [x] Successful parsing of a mock Jina AI response.
    - [x] Proper error handling for a failed API call.
7. An integration test is also created, testing its actual functionality
   - [x] We should be able to use the module to scrape one news site and have it work during the integration test. Use the canonical "example.com" for our test.
8. The Jina API interaction respects rate limits noted in `architecture.md` (20 RPM for keyless access) – for this story, this means designing the function to be callable per URL without built-in aggressive looping; scheduling/batching is Story 2.2.

## Tasks / Subtasks

- [x] Task 1: Configure News Sources (AC: #1)
  - [x] In `backend/app//core/config.py` (or a new `settings.py`):
    - [x] Define a Pydantic `Settings` model if not already present.
    - [x] Add a configuration variable (e.g., `NEWS_SOURCES: List[str]`) to hold a list of 3-5 news URLs.
    - [x] Load this list from environment variables or use a default list in the code. Example URLs: `https://www.bbc.com/news`, `https://www.reuters.com/world/`, `https://techcrunch.com/`.
  - [x] Ensure `backend/.env.example` includes `NEWS_SOURCES='["url1","url2"]'`.
- [x] Task 2: Create Jina AI Reader Service Module (AC: #2)
  - [x] Create `backend/app//data_ingestion/jina_ai_service.py`.
  - [x] Define a class or functions to encapsulate Jina AI Reader interactions.
- [x] Task 3: Implement Jina AI Reader Fetch Function (AC: #3, #4, #7)
  - [x] In `jina_ai_service.py`, create an `async` function `Workspace_article_content(url: str) -> str | None`.
  - [x] Use `httpx.AsyncClient` to make a GET request to `https://r.jina.ai/{encoded_url}`.
    - [x] Ensure the target URL is URL-encoded before appending to Jina's base URL.
    - [x] Set appropriate headers (e.g., `Accept: text/plain` or `text/markdown`, `User-Agent`).
  - [x] If the request is successful (200 OK), return the response text.
  - [x] If not successful, return `None` or raise a custom exception (see Task 4).
- [x] Task 4: Implement Error Handling for Jina API Call (AC: #5)
  - [x] Wrap the `httpx` call in `Workspace_article_content` with `try-except` blocks.
  - [x] Catch `httpx.RequestError` (network issues, timeouts) and `httpx.HTTPStatusError` (non-200 responses).
  - [x] Log errors using Python's `logging` module (e.g., `logger.error(f"Failed to fetch from Jina for URL {url}: {e}")`).
  - [x] Consider a configurable timeout for the `httpx` request.
- [x] Task 5: Implement Unit Tests for Jina Service (AC: #6)
  - [x] Create `backend/tests/unit/data_ingestion/test_jina_ai_service.py`.
  - [x] Use `pytest` and `pytest-mock` (with `mocker` fixture).
  - [x] **Test Case 1 (Success):**
    - [x] Mock `httpx.AsyncClient.get`.
    - [x] Configure the mock to return a successful response with mock article text.
    - [x] Call `Workspace_article_content` and assert it returns the expected text.
    - [x] Assert the correct Jina URL was called with correct headers.
  - [x] **Test Case 2 (HTTP Error):**
    - [x] Configure the mock `httpx.AsyncClient.get` to raise an `httpx.HTTPStatusError` (e.g., 404 or 500).
    - [x] Call `Workspace_article_content` and assert it returns `None` (or handles the error as designed) and logs the error.
  - [x] **Test Case 3 (Request Error):**
    - [x] Configure the mock `httpx.AsyncClient.get` to raise an `httpx.RequestError`.
    - [x] Call `Workspace_article_content` and assert it returns `None` (or handles the error) and logs the error.

## Dev Technical Guidance

- **Jina AI Reader Endpoint:** Use `https://r.jina.ai/` followed by the *full, URL-encoded* target article URL. Example from `architecture.md`: `https://r.jina.ai/https://www.theverge.com/2023/10/26/23933445/ai-images-news-reporting-ethics-guidelines`.
- **`httpx` Usage:**
  - Instantiate `httpx.AsyncClient()` preferably using an `async with` block for proper resource management.
  - `response = await client.get(jina_url, headers={"Accept": "text/plain", "User-Agent": "MailchimpTrendsEngine/1.0"}, timeout=30.0)`
- **Configuration (`config.py`):**

    ```python
    # backend/app//core/config.py
    from pydantic_settings import BaseSettings, SettingsConfigDict
    from typing import List

    class Settings(BaseSettings):
        NEWS_SOURCES: List[str] = [
            "[https://www.wired.com/most-recent/](https://www.wired.com/most-recent/)", # Example, choose diverse, frequently updated sources
            "[https://www.technologyreview.com/latest/](https://www.technologyreview.com/latest/)",
            "[https://www.marketingdive.com/](https://www.marketingdive.com/)"
        ]
        # ... other settings
        model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    settings = Settings()
    ```

- **Logging:** Use the standard Python `logging` module. Configure basic logging in `main.py` if not already done.

- **Rate Limiting (Design Note):** This story focuses on fetching a single URL. The function itself should not implement looping or aggressive retries beyond what `httpx` might offer if configured. The responsibility for managing rate limits across multiple URLs (e.g., by adding delays between calls) will be handled in Story 2.2 (Scheduled Fetching).

## Story Progress Notes

### Completion Notes List

### Change Log

- 2025-05-17 - Kayvan Sylvan - Initial draft
- 2025-05-19 - Kayvan Sylvan - Complete
