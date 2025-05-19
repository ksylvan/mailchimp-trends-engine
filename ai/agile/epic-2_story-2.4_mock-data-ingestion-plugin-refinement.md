# Story 2.4: Mock Data Ingestion Plugin Refinement

## Status: Draft

## Story

- As a Backend Developer Agent
- I want to refine the Mock Data Ingestion Plugin
- so that it provides realistic raw article text and metadata in a format consistent with the Jina AI Reader's output, making it a reliable data source for development, testing, and offline work.

## Acceptance Criteria (ACs)

1. The Mock Data Plugin is defined as a distinct module or set of functions within the backend's `data_ingestion` package.
2. The plugin can be configured (e.g., via a simple JSON file or hardcoded data structure for MVP) with 3-5 sample mock articles, each containing:
    - A unique `source_url` (can be a fake URL like `mock://article/1`).
    - Realistic-looking raw article `content_text` (e.g., a few paragraphs of lorem ipsum or sample marketing-related text).
    - A `Workspaceed_at` timestamp (can be static or dynamically generated).
3. The plugin provides a function (e.g., `get_mock_article_content(url: str) -> str | None` or `get_all_mock_articles() -> List[MockArticle]`) that can be called by the data ingestion process (Story 2.2 - `perform_scheduled_article_fetch`).
4. The output format of the mock data (specifically the content text) is consistent with what the Jina AI Reader (`r.jina.ai/URL`) would typically provide (e.g., plain text or Markdown).
5. The NLP processing pipeline (to be developed in Epic 3) can consume the output from this mock plugin seamlessly, as if it came from the live Jina AI Reader.
6. The main data ingestion scheduler/trigger (Story 2.2) can be easily configured (e.g., via an environment variable or a simple toggle in code/config) to use this Mock Data Plugin *instead of* the live Jina AI Reader service for development and testing.
7. Unit tests verify that the mock data plugin correctly serves the configured mock articles and metadata.

## Tasks / Subtasks

- [ ] Task 1: Define Mock Article Data Structure (AC: #2)
  - [ ] In `backend/src/mailchimp_trends/data_ingestion/mock_data_models.py` (or similar):
    - [ ] Define a Pydantic model for a mock article, e.g., `MockArticleSchema(BaseModel)` with fields like `source_url: str`, `content_text: str`, `Workspaceed_at: datetime`.
  - [ ] Create a sample data source (e.g., `backend/src/mailchimp_trends/data_ingestion/mock_articles_data.json` or a Python list of `MockArticleSchema` instances within a `.py` file).
    - [ ] Populate with 3-5 diverse mock articles. Ensure `content_text` is substantial enough for basic NLP testing later.
- [ ] Task 2: Implement Mock Data Service (AC: #1, #3, #4)
  - [ ] Create `backend/src/mailchimp_trends/data_ingestion/mock_data_service.py`.
  - [ ] Implement a function `load_mock_articles() -> List[MockArticleSchema]` to load data from the JSON file or return the hardcoded list.
  - [ ] Implement `get_mock_article_by_url(url: str, mock_articles: List[MockArticleSchema]) -> MockArticleSchema | None`.
  - [ ] Implement `get_all_mock_articles(mock_articles: List[MockArticleSchema]) -> List[MockArticleSchema]`.
  - [ ] Ensure `content_text` served by these functions is in a format (plain text or simple Markdown) that mimics Jina's output and is ready for NLP.
- [ ] Task 3: Integrate Mock Plugin Toggle into Ingestion Process (AC: #6)
  - [ ] In `backend/src/mailchimp_trends/core/config.py`:
    - [ ] Add a new setting: `USE_MOCK_DATA_INGESTION: bool = False` (load from env var `USE_MOCK_DATA_INGESTION`).
    - [ ] Update `backend/.env.example` with `USE_MOCK_DATA_INGESTION=False`.
  - [ ] Modify `perform_scheduled_article_fetch` in `backend/src/mailchimp_trends/data_ingestion/scheduler.py` (from Story 2.2):
    - [ ] Check `settings.USE_MOCK_DATA_INGESTION`.
    - [ ] If `True`:
      - [ ] Load mock articles using `mock_data_service.load_mock_articles()`.
      - [ ] Iterate through these mock articles. For each, use its `content_text` and `source_url` to save to the database via `content_store_service.save_raw_article` (as if it came from Jina). Log appropriately.
      - [ ] No need for delays or actual Jina API calls in this branch.
    - [ ] If `False`: Proceed with the existing Jina AI Reader fetching logic.
- [ ] Task 4: Ensure Consumability by NLP (AC: #5)
  - [ ] This is primarily a design consideration. The `content_text` from mock data should be raw text suitable for the NLP pipeline (Epic 3). No special pre-processing specific to mock data should be needed by the NLP module.
- [ ] Task 5: Implement Unit Tests for Mock Data Service (AC: #7)
  - [ ] Create `backend/tests/unit/data_ingestion/test_mock_data_service.py`.
  - [ ] Test `load_mock_articles` to ensure it loads the data correctly.
  - [ ] Test `get_mock_article_by_url` for successful retrieval and for a non-existent URL.
  - [ ] Test `get_all_mock_articles`.
  - [ ] Verify the structure and content of the returned mock articles match expectations.

## Dev Technical Guidance

- **Mock Data Content:** The mock article text should be varied enough to be useful for testing different aspects of the NLP pipeline later (e.g., different topics, sentiments if possible). For MVP, a few paragraphs of generic text per article is fine.
- **Configuration Toggle:** The `USE_MOCK_DATA_INGESTION` flag in `config.py` (sourced from an environment variable) is a clean way to switch between live and mock data ingestion.
- **Consistency with Jina Output:** The key is that `content_text` from the mock plugin should be in the same fundamental format (raw text or Markdown string) that `jina_ai_service.fetch_article_content` would return. This ensures the downstream `content_store_service` and NLP pipeline treat it identically.
- **No Need to Mock `httpx` Here:** This plugin *replaces* the Jina call, so you're testing the plugin's own logic, not its interaction with a (mocked) external service.
- **Storage Integration:** The mock data flow should still use the `content_store_service.save_raw_article` function to ensure data lands in the database correctly, just like real data would.

## Story Progress Notes

### Completion Notes List

{Any notes about implementation choices, difficulties, or follow-up needed}

### Change Log

2025-05-17 - Kayvan Sylvan - Initial draft
