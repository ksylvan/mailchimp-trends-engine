# Story 3.1: Basic NLP Preprocessing

## Status: Draft

## Story

- As a Backend Developer Agent
- I want to implement a basic NLP preprocessing pipeline for the raw textual content fetched from articles
- so that the text is cleaned and standardized, preparing it for effective topic extraction and sentiment analysis.

## Acceptance Criteria (ACs)

1. A new backend module (e.g., `nlp_processing/`) is created or utilized for NLP tasks.
2. The NLP preprocessing pipeline includes the following steps:
    - Text cleaning (e.g., removing HTML tags if present, special characters, normalizing whitespace).
    - Tokenization (splitting text into individual words/tokens).
    - Stop word removal (removing common words like "the", "is", "in").
    - Lemmatization or Stemming (reducing words to their base/root form; lemmatization preferred if performance allows).
3. A well-regarded Python NLP library (e.g., `spaCy` or `NLTK`, as per architectural discussions favoring Hugging Face ecosystem, `spaCy` is a good choice for preprocessing if not using HF tokenizers directly for everything) is used to implement these steps.
4. The output of the preprocessing pipeline for a given raw text input is a list of clean, relevant tokens (or a string of joined clean tokens).
5. Unit tests are implemented to verify each step of the preprocessing pipeline with sample text inputs.
6. The preprocessing function(s) can handle empty or very short text inputs gracefully (e.g., returning an empty list of tokens).

## Tasks / Subtasks

- [ ] Task 1: Setup NLP Library and Module (AC: #1, #3)
  - [ ] Add chosen NLP library (e.g., `spacy`) to `backend/pyproject.toml` and update environment using `uv sync`.
  - [ ] Download necessary language models for spaCy (e.g., `python -m spacy download en_core_web_sm`). Document this step in `backend/README.md` or a setup script.
  - [ ] Create `backend/app//nlp_processing/preprocessing_service.py`.
- [ ] Task 2: Implement Text Cleaning Function (AC: #2a)
  - [ ] In `preprocessing_service.py`, create `def clean_text(raw_text: str) -> str:`.
  - [ ] Implement logic to:
    - [ ] Remove HTML tags (e.g., using `BeautifulSoup` if complex HTML is expected, or simpler regex if only basic tags). For MVP, assume Jina Reader provides mostly clean text or Markdown; focus on basic cleaning.
    - [ ] Remove or normalize special characters (e.g., keeping alphanumeric, spaces, basic punctuation relevant for NLP).
    - [ ] Normalize whitespace (e.g., replace multiple spaces/newlines with a single space).
    - [ ] Convert text to lowercase.
- [ ] Task 3: Implement Tokenization, Stop Word Removal, and Lemmatization (AC: #2b, #2c, #2d)
  - [ ] In `preprocessing_service.py`, create `def preprocess_text(text: str) -> List[str]:` (or similar, name it `get_processed_tokens`).
  - [ ] Load the spaCy language model (e.g., `nlp = spacy.load("en_core_web_sm")`).
  - [ ] Process the input `text` with the spaCy pipeline.
  - [ ] Iterate through tokens:
    - [ ] Filter out stop words (e.g., `if not token.is_stop`).
    - [ ] Filter out punctuation (e.g., `if not token.is_punct`).
    - [ ] Get the lemma of the token (e.g., `token.lemma_`).
    - [ ] Collect valid lemmas.
- [ ] Task 4: Implement Main Preprocessing Function (AC: #4, #6)
  - [ ] In `preprocessing_service.py`, create `def get_clean_tokens(raw_text: str) -> List[str]:`.
  - [ ] This function will call `clean_text()` then `preprocess_text()`.
  - [ ] Ensure it handles empty or `None` input gracefully, returning an empty list.
- [ ] Task 5: Implement Unit Tests (AC: #5)
  - [ ] Create `backend/tests/unit/nlp_processing/test_preprocessing_service.py`.
  - [ ] Test `clean_text` with various inputs (HTML, extra spaces, special chars).
  - [ ] Test `preprocess_text` (or `get_processed_tokens` directly if it incorporates cleaning):
    - [ ] Verify tokenization.
    - [ ] Verify stop word removal.
    - [ ] Verify lemmatization (e.g., "running" -> "run").
    - [ ] Verify punctuation removal.
  - [ ] Test `get_clean_tokens` with end-to-end examples, including empty/null string inputs.

## Dev Technical Guidance

- **NLP Library Choice:** `spaCy` is a good choice for efficient and robust preprocessing. Ensure the small English model (`en_core_web_sm`) is sufficient for lemmatization and stop word lists for MVP. If more complex preprocessing is needed later, a larger model could be used.
- **HTML Cleaning:** Jina AI Reader often provides Markdown or clean text. If HTML cleaning is needed, `BeautifulSoup4` (`bs4`) is a standard Python library. For MVP, simple regex might suffice if HTML presence is minimal and basic. Let's assume Jina provides mostly clean text so `clean_text` can focus on simpler normalization.
- **Lemmatization vs. Stemming:** Lemmatization (e.g., `token.lemma_` in spaCy) generally produces more linguistically correct base forms than stemming and is preferred.
- **Efficiency:** For processing many documents, loading the spaCy model (`spacy.load()`) once and reusing the `nlp` object is more efficient than reloading it for each document. Consider how this service class/module might be instantiated or how the model might be loaded globally if performance becomes an issue with frequent calls. For individual text preprocessing, loading it inside the function is fine for now.
- **Return Type:** Returning a list of clean string tokens is a versatile output for subsequent NLP tasks.
- **Stop Word Customization:** Default stop word lists are usually fine, but if specific domain stop words become apparent, spaCy allows customizing the stop word list. Not required for MVP.

## Story Progress Notes

### Completion Notes List

### Change Log

- 2025-05-17 - Kayvan Sylvan - Initial draft
