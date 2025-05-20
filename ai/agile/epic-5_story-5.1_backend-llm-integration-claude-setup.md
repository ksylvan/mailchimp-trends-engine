# Story 5.1: Backend LLM Integration Design (Pluggable) & Claude Setup

## Status: Draft

## Story

- As a Backend Developer Agent
- I want to design a generic Large Language Model (LLM) service interface within the backend and implement an initial concrete service for Anthropic Claude
- so that the system can integrate with Claude for marketing content generation, while maintaining flexibility to support other LLM providers in the future.

## Acceptance Criteria (ACs)

1. A generic LLM service interface (e.g., an abstract base class or a Python protocol) is defined in the backend (e.g., in `llm_integration/llm_service_protocol.py`). This interface specifies a common method for generating text-based content (e.g., `async def generate_content(prompt: str, max_tokens: int) -> str:`).
2. A concrete implementation, `ClaudeLLMService`, is created that implements the generic LLM service interface.
3. The `anthropic` Python SDK is added as a backend dependency.
4. The `ClaudeLLMService` securely accesses the Anthropic Claude API key from environment variables/configuration (as per `architecture.md` "Secrets Management").
5. The `ClaudeLLMService` can make a basic test call to the Claude API (e.g., a simple "hello world" type prompt) and successfully receive a response. This verifies API key validity and basic connectivity.
6. Error handling for Claude API calls (e.g., authentication errors, rate limits, server errors) is implemented within `ClaudeLLMService`, logging errors and potentially raising custom exceptions.
7. Unit tests are created for `ClaudeLLMService`, mocking the Anthropic SDK client, to verify:
    - Correct API request construction.
    - Successful response parsing.
    - Proper error handling for various API error scenarios.

## Tasks / Subtasks

- [ ] Task 1: Define Generic LLM Service Interface (AC: #1)
  - [ ] Create `backend/app//llm_integration/llm_service_protocol.py`.
  - [ ] Define a `typing.Protocol` or an `abc.ABC` for the LLM service.

        ```python
        # llm_service_protocol.py
        from typing import Protocol, runtime_checkable

        @runtime_checkable
        class LLMServiceProtocol(Protocol):
            async def generate_content(self, prompt: str, max_tokens: int = 1024) -> str: # Or a more structured response
                ...
        ```

- [ ] Task 2: Add Anthropic SDK Dependency (AC: #3)
  - [ ] Add `anthropic` to `backend/pyproject.toml` and run `uv sync`.
- [ ] Task 3: Implement `ClaudeLLMService` (AC: #2, #4, #6)
  - [ ] Create `backend/app//llm_integration/claude_service.py`.
  - [ ] Implement `class ClaudeLLMService(LLMServiceProtocol):`.
    - [ ] In `__init__`, load the `CLAUDE_API_KEY` from `core.config.settings`. Raise an error if not found.
    - [ ] Initialize the `anthropic.AsyncAnthropic` client with the API key.
    - [ ] Implement `async def generate_content(self, prompt: str, max_tokens: int = 1500) -> str:`.
      - [ ] Construct the message payload for the Claude API (model: `claude-3-haiku-20240307` for MVP, messages list with user role and prompt).
      - [ ] Make the API call using `await self.client.messages.create(...)`.
      - [ ] Handle potential exceptions from the SDK (e.g., `anthropic.APIConnectionError`, `anthropic.RateLimitError`, `anthropic.AuthenticationError`, `anthropic.APIStatusError`). Log errors and potentially re-raise as custom application exceptions (e.g., `LLMGenerationError`).
      - [ ] Parse the successful response to extract the generated text content.
      - [ ] Return the extracted text.
- [ ] Task 4: Implement Basic Test Call Logic (AC: #5)
  - [ ] Add a simple, private test method or a separate script that uses `ClaudeLLMService` to make a very basic call (e.g., "Why is the sky blue?") to ensure the API key and setup are working. This is for initial developer verification, not part of the main application flow. Alternatively, this can be verified during initial unit testing with a live (dev) key.
- [ ] Task 5: Configure Claude API Key (AC: #4)
  - [ ] Ensure `CLAUDE_API_KEY` is added to `backend/.env.example`.
  - [ ] Add `CLAUDE_API_KEY: Optional[str] = None` to `core/config.py Settings` model.
  - [ ] The developer/user will need to set their actual key in their `.env` file.
- [ ] Task 6: Implement Unit Tests for `ClaudeLLMService` (AC: #7)
  - [ ] Create `backend/tests/unit/llm_integration/test_claude_service.py`.
  - [ ] Use `pytest` and `pytest-mock` (`mocker`).
  - [ ] Mock the `anthropic.AsyncAnthropic` client and its `messages.create` method.
  - [ ] **Test Case 1 (Successful Generation):**
    - [ ] Configure `messages.create` mock to return a successful `Message` object.
    - [ ] Call `claude_service.generate_content` and assert it returns the expected text.
    - [ ] Verify correct parameters were passed to `messages.create` (model, max_tokens, messages).
  - [ ] **Test Case 2 (API Authentication Error):**
    - [ ] Configure `messages.create` mock to raise `anthropic.AuthenticationError`.
    - [ ] Call `claude_service.generate_content` and assert that it handles the error appropriately (e.g., raises a custom `LLMGenerationError` or returns a specific error indicator, and logs the error).
  - [ ] **Test Case 3 (Rate Limit Error):**
    - [ ] Configure `messages.create` mock to raise `anthropic.RateLimitError`.
    - [ ] Assert appropriate error handling and logging.
  - [ ] **Test Case 4 (Other API Error):**
    - [ ] Configure `messages.create` mock to raise `anthropic.APIStatusError`.
    - [ ] Assert appropriate error handling and logging.
  - [ ] Test instantiation failure if API key is missing.

## Dev Technical Guidance

- **Anthropic SDK Usage:** Refer to the official Anthropic Python SDK documentation for `AsyncAnthropic` and `messages.create`.
  - Model for MVP: `claude-3-haiku-20240307` (cost-effective).
  - Request structure for `messages.create`:

        ```json
        {
            "model": "claude-3-haiku-20240307",
            "max_tokens": 1500, // Or as passed to the function
            "messages": [{"role": "user", "content": "Your prompt here"}]
        }
        ```

  - Response parsing: The generated text is typically in `response.content[0].text`.
- **Protocol vs. ABC:** Python's `typing.Protocol` is good for structural subtyping (duck typing with type checking). `abc.ABC` is for nominal subtyping (requires explicit inheritance). For a service interface, `Protocol` is often more flexible.
- **Configuration:** API Key must be loaded securely via `core.config.settings` and never hardcoded.
- **Error Handling:** Define custom exceptions (e.g., `LLMConnectionError`, `LLMAuthenticationError`, `LLMGenerationError`) in `llm_integration/exceptions.py` to abstract away specific SDK exceptions if needed, making the rest of the application less coupled to Anthropic's SDK.
- **Efficiency:** The `AsyncAnthropic` client should ideally be instantiated once per `ClaudeLLMService` instance. If `ClaudeLLMService` is a singleton or managed by DI, this is efficient.

## Story Progress Notes

### Completion Notes List

### Change Log

- 2025-05-17 - Kayvan Sylvan - Initial draft
