# Story 3.3: Basic Sentiment Analysis

## Status: Draft

## Story

- As a Backend Developer Agent
- I want to integrate a pre-trained Hugging Face model to perform basic sentiment analysis (positive, negative, neutral) on preprocessed article text or topic snippets
- so that the identified marketing trends can be enriched with sentiment information.

## Acceptance Criteria (ACs)

1. A suitable pre-trained sentiment analysis model from the Hugging Face Hub is selected (e.g., a model fine-tuned for sentiment classification of general text or news).
2. The `transformers` library is utilized for this integration.
3. A function is implemented in the `nlp_processing` module that takes preprocessed text (or a list of topics, TBD which is better input for trend sentiment) as input.
4. This function uses the selected Hugging Face model/pipeline to determine the sentiment (e.g., "positive", "negative", "neutral") of the input.
5. The determined sentiment is stored in the `ProcessedArticleDataModel` (e.g., in an `overall_sentiment` field).
6. Unit tests are implemented to verify the sentiment analysis function, using mock input text and a mocked Hugging Face pipeline/model response.
7. The system handles cases where sentiment cannot be confidently determined (e.g., defaults to "neutral" or stores as null).

## Tasks / Subtasks

- [ ] Task 1: Research and Select Hugging Face Sentiment Model (AC: #1)
  - [ ] Explore Hugging Face Hub for suitable sentiment analysis models. Look for models trained on general text, news, or social media that output positive/negative/neutral classifications.
  - [ ] *Initial Suggestion: `distilbert-base-uncased-finetuned-sst-2-english` (outputs positive/negative, may need mapping to neutral or choosing another model for 3-class), or a dedicated 3-class sentiment model like `cardiffnlp/twitter-roberta-base-sentiment-latest` (outputs label_0, label_1, label_2 which map to neg, neu, pos).*
  - [ ] Document the chosen model name in `nlp_processing/sentiment_analysis_service.py`.
- [ ] Task 2: Implement Sentiment Analysis Service (AC: #2, #3, #4, #7)
  - [ ] Create `backend/src/mailchimp_trends/nlp_processing/sentiment_analysis_service.py`.
  - [ ] Initialize the Hugging Face pipeline for sentiment analysis (e.g., `pipeline("sentiment-analysis", model="chosen_model_name")`). Load once for efficiency.
  - [ ] Implement `async def analyze_sentiment(text_or_tokens: Union[str, List[str]]) -> str:` (e.g., returning "positive", "negative", "neutral").
    - [ ] If input is a list of tokens, join them to a string.
    - [ ] Pass the text to the pipeline.
    - [ ] Process the model's output. Many models return `[{'label': 'POSITIVE', 'score': 0.99}]` or similar. Map the label to your desired output strings ("positive", "negative", "neutral").
    - [ ] If the model only provides positive/negative, decide on a threshold for score to classify as neutral, or default to neutral if scores are low for both, or choose a 3-class model. For MVP, a 3-class model is simpler if available and good. If using a 2-class model, a simple approach: if score for POSITIVE > 0.6 return "positive", if score for NEGATIVE > 0.6 return "negative", else "neutral".
    - [ ] Handle potential errors or low-confidence outputs gracefully (e.g., default to "neutral").
- [ ] Task 3: Integrate Sentiment Storage into Data Processing Flow (AC: #5)
  - [ ] Update `ProcessedArticleDataModel` in `backend/src/mailchimp_trends/db/models_db.py` to include `overall_sentiment = Column(String, nullable=True)`.

        ```python
        # backend/src/mailchimp_trends/db/models_db.py
        # class ProcessedArticleDataModel(Base):
        #    # ... other fields
        #    overall_sentiment = Column(String, nullable=True) # e.g., "positive", "negative", "neutral"
        ```

  - [ ] In `nlp_processing/nlp_service.py`'s `process_article` method:
    - [ ] After preprocessing and topic extraction, call `sentiment_analysis_service.analyze_sentiment(cleaned_text_or_tokens)`. *Decision: Analyze sentiment of the whole cleaned article text for overall article sentiment for MVP.*
    - [ ] Store the returned sentiment in the `overall_sentiment` field of the `ProcessedArticleDataModel` instance.
    - [ ] Update the save operation for `ProcessedArticleDataModel`.
- [ ] Task 4: Implement Unit Tests (AC: #6)
  - [ ] Create `backend/tests/unit/nlp_processing/test_sentiment_analysis_service.py`.
  - [ ] Mock the Hugging Face `pipeline` call.
  - [ ] Test `analyze_sentiment`:
    - [ ] Provide sample text inputs.
    - [ ] Configure the mock pipeline to return sample sentiment analysis outputs (e.g., `[{'label': 'POSITIVE', 'score': 0.99}]`, `[{'label': 'LABEL_2', 'score': 0.9}]` if using a 3-class model like RoBERTa).
    - [ ] Assert that the function correctly parses the output and returns the expected sentiment string ("positive", "negative", "neutral").
    - [ ] Test with inputs that might result in low confidence or default sentiment.
  - [ ] Update tests for `nlp_service.process_article` to verify it calls the sentiment service and stores the sentiment correctly.

## Dev Technical Guidance

- **Model Selection:** The choice of model impacts how you interpret the output. Some models are binary (positive/negative), others are multi-class (positive/negative/neutral). Check the model card on Hugging Face Hub for its specific output labels and recommended usage. `cardiffnlp/twitter-roberta-base-sentiment-latest` is a popular choice for 3-class sentiment.
- **Input for Sentiment Analysis:** For MVP, performing sentiment analysis on the entire preprocessed article text is a reasonable starting point to get an "overall article sentiment." Analyzing sentiment per topic could be a more granular future enhancement.
- **Mapping Labels:** If the model returns labels like `LABEL_0`, `LABEL_1`, `LABEL_2` or `POS`, `NEG`, `NEU`, ensure you have a clear mapping in your service to your desired output strings ("positive", "negative", "neutral").
- **Model Loading:** Similar to the topic model, load the sentiment analysis pipeline once for efficiency.
- **Configuration:** If thresholds for sentiment scores (if not using a direct 3-class model) are used, make these configurable in `core/config.py`.

## Story Progress Notes

### Completion Notes List

{Any notes about implementation choices, difficulties, or follow-up needed}

### Change Log

2025-05-17 - Kayvan Sylvan - {Description of Change, e.g., "Story Drafted"}
