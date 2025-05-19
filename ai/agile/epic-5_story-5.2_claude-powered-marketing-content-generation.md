# Story 5.2: Claude-Powered Marketing Content Generation Logic

## Status: Draft

## Story

- As a Backend Developer Agent
- I want to implement the logic for generating relevant marketing content ideas (email subject lines, body copy, campaign themes) using the Claude LLM service based on a selected trend
- so that the system can provide actionable AI-generated content to the user via an API endpoint.

## Acceptance Criteria (ACs)

1. A new backend API endpoint (e.g., `POST /api/v1/trends/{trend_id}/generate-content-ideas`) is created.
2. This endpoint retrieves details of the specified `trend_id` from the database (e.g., trend name, summary, associated topics, sentiment).
3. Effective prompts are engineered to instruct the Claude LLM (via `ClaudeLLMService` from Story 5.1) to generate:
    - 2-3 email subject line ideas.
    - 1 short paragraph (2-3 sentences) of engaging email body copy.
    - 1 campaign theme idea.
    (These requirements are from PRD FR4).
4. The `ClaudeLLMService.generate_content()` method is called with the engineered prompt.
5. The response from Claude is parsed, and the generated content ideas are structured (e.g., into a Pydantic model).
6. The API endpoint returns the structured, generated content to the client.
7. Unit tests are implemented for the prompt engineering logic and the service layer that orchestrates trend data retrieval, prompt generation, LLM call, and response parsing. These tests will use a mocked `ClaudeLLMService` and mock trend data.
8. Error handling is implemented for cases where the trend ID is not found or the LLM service fails.

## Tasks / Subtasks

- [ ] Task 1: Define Request/Response Schemas for Content Generation (AC: #5, #6)
  - [ ] In `backend/src/mailchimp_trends/schemas/llm_schemas.py` (or similar):
    - [ ] Define `GeneratedContentIdeasSchema(BaseModel)`:
      - `email_subject_lines: List[str]`
      - `email_body_copy: str`
      - `campaign_themes: List[str]` (changed to List based on PRD FR4, Story 5.2 prompt details)
    - [ ] Define `GenerateContentResponseSchema(BaseModel)`:
      - `trend_id: str`
      - `trend_name: str`
      - `generated_content: GeneratedContentIdeasSchema`
  - [ ] The API will use `GenerateContentResponseSchema` for its response. No request body is needed for MVP as per `architecture.md` API spec (uses trend_id from path).
- [ ] Task 2: Implement API Endpoint for Content Generation (AC: #1)
  - [ ] Create a new router, e.g., `backend/src/mailchimp_trends/api/v1/llm_router.py`.
  - [ ] Implement `POST /trends/{trend_id}/generate-content-ideas` endpoint.
  - [ ] This endpoint will depend on a new service function (see Task 3).
- [ ] Task 3: Implement Content Generation Service Logic (AC: #2, #3, #4, #8)
  - [ ] In `backend/src/mailchimp_trends/llm_integration/content_generation_service.py`:
    - [ ] Create `async def generate_marketing_content_for_trend(db: AsyncSession, llm_service: LLMServiceProtocol, trend_id: int) -> GenerateContentResponseSchema:`. (Note: `trend_id` is likely `int` if it's the PK from `MarketingTrendModel`).
    - [ ] Fetch `MarketingTrendModel` data from DB using `trend_id`. Handle "not found" errors (raise HTTPException 404).
    - [ ] **Prompt Engineering (Crucial):**
      - Develop a prompt template that incorporates trend details (name, summary, key topics, sentiment) to guide Claude.
      - Example prompt structure:

                ```
                Human: Based on the marketing trend titled "{trend_name}", which has a general sentiment of "{trend_sentiment}" and is summarized as "{trend_summary}", and related to topics like {trend_topics_str}. Please generate the following for a Mailchimp marketing campaign:
                1.  Three concise and distinct email subject line ideas.
                2.  One short paragraph (2-3 sentences) of engaging email body copy that could be used in an email campaign.
                3.  One overall campaign theme idea that captures the essence of this trend for marketing purposes.

                Please structure your response clearly, for example:
                Email Subject Lines:
                - Subject 1
                - Subject 2
                - Subject 3
                Email Body Copy:
                - [The paragraph]
                Campaign Themes:
                - Theme 1

                Assistant:
                ```

    - [ ] Call `await llm_service.generate_content(prompt=engineered_prompt, max_tokens=...)`.
      - Choose appropriate `max_tokens` (e.g., 500-1000 to be safe for the requested content length).
    - [ ] Handle exceptions from `llm_service.generate_content` (e.g., log and raise HTTPException 503 or 500).
- [ ] Task 4: Implement Response Parsing from LLM Output (AC: #5)
  - [ ] In `content_generation_service.py`, add logic to parse the raw string response from Claude.
  - [ ] Extract the subject lines, body copy, and campaign themes based on the expected structure solicited in the prompt. This might involve regex or simple string splitting. *Aim for a robust parsing method.*
  - [ ] Populate the `GeneratedContentIdeasSchema` with the parsed content.
- [ ] Task 5: Wire up Endpoint, Service, and Dependencies (AC: #6)
  - [ ] Ensure `ClaudeLLMService` can be injected (e.g., via FastAPI `Depends`) into `content_generation_service.py` functions or the API endpoint.
  - [ ] The API endpoint in `llm_router.py` calls `content_generation_service.generate_marketing_content_for_trend`.
  - [ ] Return the `GenerateContentResponseSchema`.
- [ ] Task 6: Implement Unit Tests (AC: #7)
  - [ ] Create `backend/tests/unit/llm_integration/test_content_generation_service.py`.
  - [ ] Mock `db` session and functions to fetch trend data.
  - [ ] Mock `LLMServiceProtocol.generate_content` method.
  - [ ] **Test Case 1 (Successful Generation & Parsing):**
    - [ ] Provide mock trend data.
    - [ ] Configure mock `generate_content` to return a well-structured string response that your parser can handle.
    - [ ] Call `generate_marketing_content_for_trend`.
    - [ ] Assert the prompt sent to the LLM service is correctly engineered.
    - [ ] Assert the returned `GenerateContentResponseSchema` contains correctly parsed data.
  - [ ] **Test Case 2 (LLM Service Error):**
    - [ ] Configure mock `generate_content` to raise an exception.
    - [ ] Assert that `generate_marketing_content_for_trend` handles this (e.g., raises an appropriate HTTPException).
  - [ ] **Test Case 3 (Trend Not Found):**
    - [ ] Configure mock DB call to return no trend.
    - [ ] Assert that `generate_marketing_content_for_trend` raises HTTPException 404.
  - [ ] **Test Case 4 (LLM Output Parsing Variations/Failures):**
    - [ ] Test with slightly malformed LLM string outputs to check robustness of the parser (e.g., if it returns fewer than 3 subjects).

## Dev Technical Guidance

- **Prompt Engineering:** This is key. The prompt must be very clear to Claude about the desired output structure (subjects, body, themes) and the type of content. Iteration on the prompt will likely be needed. The example in Tasks is a starting point.
- **Response Parsing:** Parsing free-form text from an LLM can be brittle.
  - Instruct the LLM in the prompt to use clear delimiters or headings (e.g., "Email Subject Lines:\n- ...").
  - Use regex or string manipulation. Be prepared for slight variations. For MVP, a best-effort parsing is acceptable. If Claude API offers structured output modes in the future, prefer those.
- **Max Tokens:** Set `max_tokens` in the call to `llm_service.generate_content` high enough to accommodate the requested content items.
- **Error Handling:** If parsing fails, the API should return a meaningful error (e.g., 500, with a log indicating parsing failure).
- **Trend Details for Prompt:** Fetch necessary details from `MarketingTrendModel` (name, score) and potentially associated `ProcessedArticleDataModel` (topics, overall_sentiment) to enrich the prompt.
- **Dependency Injection:** Use FastAPI's `Depends` to inject the database session and the `LLMServiceProtocol` implementation into the service layer or endpoint.

        ```python
        # Example of LLMServiceProtocol dependency
        # from mailchimp_trends.llm_integration.claude_service import ClaudeLLMService
        # from mailchimp_trends.llm_integration.llm_service_protocol import LLMServiceProtocol
        # def get_llm_service() -> LLMServiceProtocol:
        #     return ClaudeLLMService() # This could be more sophisticated with settings later
        #
        # # In your service function or endpoint:
        # llm_service: LLMServiceProtocol = Depends(get_llm_service)
        ```

## Story Progress Notes

### Completion Notes List

{Any notes about implementation choices, difficulties, or follow-up needed}

### Change Log

- 2025-05-17 - Kayvan Sylvan - Initial draft
