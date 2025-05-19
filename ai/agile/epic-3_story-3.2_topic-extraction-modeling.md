# Story 3.2: Topic Extraction/Modeling

## Status: Draft

## Story

- As a Backend Developer Agent
- I want to integrate a pre-trained Hugging Face transformer model to perform topic extraction/modeling on the preprocessed article text
- so that key themes and subjects discussed in the articles can be identified and stored for trend analysis.

## Acceptance Criteria (ACs)

1. A suitable pre-trained topic modeling or keyword extraction model from the Hugging Face Hub is selected (e.g., a model fine-tuned for news summarization, keyword extraction, or zero-shot classification that can identify topics).
2. The selected Hugging Face `transformers` library is added as a dependency and configured in the backend.
3. A function is implemented in the `nlp_processing` module that takes preprocessed text (list of clean tokens or a clean string from Story 3.1) as input.
4. This function uses the selected Hugging Face model/pipeline to extract a list of relevant topics/keywords (e.g., top 3-5 topics) from the input text.
5. The extracted topics/keywords are stored in the `ProcessedArticleDataModel` (e.g., in the `topics` JSON field) associated with the raw article.
6. Basic unit tests are implemented to verify the topic extraction function, using mock preprocessed text and a mocked Hugging Face pipeline/model response.
7. The system handles cases where the model might not return any topics for very short or ambiguous text.

## Tasks / Subtasks

- [ ] Task 1: Research and Select Hugging Face Model (AC: #1)
  - [ ] Explore Hugging Face Hub for suitable models. Candidates:
    - Zero-shot classification models (e.g., `facebook/bart-large-mnli`): Can classify text against a predefined list of candidate topics.
    - Keyword extraction models.
    - Models good at text summarization might also yield good topic-like phrases.
  - [ ] For MVP, select a relatively lightweight but effective model. *Initial Suggestion: A zero-shot classification model with a predefined list of general marketing-related topics could be a good start.*
  - [ ] Document the chosen model name (e.g., in `nlp_processing/topic_model_service.py`).
- [ ] Task 2: Add Dependencies and Configure (AC: #2)
  - [ ] Add `transformers` and `torch` (or `tensorflow` if model requires it) to `backend/pyproject.toml` and update environment using `uv sync`.
  - [ ] Ensure any necessary model files are downloaded during first use or as part of setup (Hugging Face libraries usually handle this automatically by caching to `~/.cache/huggingface/`).
- [ ] Task 3: Implement Topic Extraction Service (AC: #3, #4, #7)
  - [ ] Create `backend/src/mailchimp_trends/nlp_processing/topic_model_service.py`.
  - [ ] Initialize the Hugging Face pipeline for the chosen task (e.g., `pipeline("zero-shot-classification", model="chosen_model_name")`).
    - [ ] Consider loading the pipeline once (e.g., as a global variable or in a class constructor) for efficiency if the service is called frequently.
  - [ ] Implement `async def extract_topics(cleaned_text_or_tokens: Union[str, List[str]]) -> List[str]:`.
    - [ ] If input is a list of tokens, join them into a string if the model expects a string.
    - [ ] Pass the text to the pipeline.
      - [ ] For zero-shot classification: Provide a list of `candidate_labels` (predefined topics, e.g., ["AI in marketing", "social media trends", "content strategy", "SEO updates", "email marketing innovations"]). These labels can be configurable.
    - [ ] Process the model's output to get the top N topics/labels with the highest scores.
    - [ ] Return a list of topic strings. Handle cases where no topics are confidently identified by returning an empty list.
- [ ] Task 4: Integrate Topic Storage into Data Processing Flow (AC: #5)
  - [ ] Create/Update `ProcessedArticleDataModel` in `backend/src/mailchimp_trends/db/models_db.py` to ensure it has a `topics = Column(JSON, nullable=True)` field.

        ```python
        # backend/src/mailchimp_trends/db/models_db.py
        # class ProcessedArticleDataModel(Base):
        #    # ... other fields
        #    topics = Column(JSON, nullable=True) # Stores List[str]
        ```

  - [ ] Create a new service, e.g., `backend/src/mailchimp_trends/nlp_processing/nlp_service.py`, that orchestrates preprocessing, topic extraction, and (later) sentiment analysis.
  - [ ] This `nlp_service` will have a method like `async def process_article(db: AsyncSession, raw_article: RawArticleModel) -> ProcessedArticleDataModel:`.
    - [ ] Call `preprocessing_service.get_clean_tokens(raw_article.content_text)`.
    - [ ] Call `topic_model_service.extract_topics(cleaned_tokens_or_text)`.
    - [ ] (Later add sentiment analysis call here).
    - [ ] Create or update a `ProcessedArticleDataModel` instance, linking it to `raw_article.id` and storing the extracted `topics`.
    - [ ] Save the `ProcessedArticleDataModel` to the database.
- [ ] Task 5: Implement Unit Tests (AC: #6)
  - [ ] Create `backend/tests/unit/nlp_processing/test_topic_model_service.py`.
  - [ ] Mock the Hugging Face `pipeline` call or the model's direct call.
  - [ ] Test `extract_topics`:
    - [ ] Provide sample preprocessed text.
    - [ ] Configure the mock pipeline to return a sample model output.
    - [ ] Assert that the function correctly parses this output and returns the expected list of topic strings.
    - [ ] Test with input that should result in no topics being extracted.
  - [ ] Test the `nlp_service.process_article` integration:
    - [ ] Mock preprocessing and topic extraction service calls.
    - [ ] Verify it calls them correctly and saves a `ProcessedArticleDataModel` with the expected topics.

## Dev Technical Guidance

- **Hugging Face Pipeline:** The `pipeline()` function from the `transformers` library is the easiest way to use pre-trained models for standard tasks like zero-shot classification or feature extraction.
- **Zero-Shot Classification for Topics:** This is a flexible approach. You'll need a predefined list of `candidate_labels` that represent the types of topics you're interested in. This list can be made configurable (e.g., in `core/config.py`). The model will then score how well the input text matches each candidate label.

        ```python
        # Example usage (conceptual)
        # from transformers import pipeline
        # classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
        # sequence_to_classify = "Apple just announced the new iPhone 15."
        # candidate_labels = ['technology', 'politics', 'sports', 'finance']
        # result = classifier(sequence_to_classify, candidate_labels)
        # print(result['labels'], result['scores'])
        ```

- **Model Loading:** Hugging Face models can be large. They are downloaded and cached on first use. For a service, loading the model/pipeline once when the application starts or when the service class is instantiated is crucial for performance.

- **Storing Topics:** The `topics` field in `ProcessedArticleDataModel` is `JSON`. Store the list of topic strings directly (e.g., `["AI in marketing", "SEO updates"]`).
- **Candidate Labels Configuration:** The list of candidate topic labels for zero-shot classification should be configurable, perhaps in `core/config.py`, to allow easy tuning of what topics the system looks for.

        ```python
        # core/config.py
        # CANDIDATE_TOPIC_LABELS: List[str] = ["AI in marketing", "social media trends", ...]
        ```

## Story Progress Notes

### Completion Notes List

{Any notes about implementation choices, difficulties, or follow-up needed}

### Change Log

2025-05-17 - Kayvan Sylvan - {Description of Change, e.g., "Story Drafted"}
