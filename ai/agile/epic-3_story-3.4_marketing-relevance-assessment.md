# Story 3.4: Marketing Relevance Assessment (Initial Pass)

## Status: Draft

## Story

- As a Backend Developer
- I want to implement an initial pass for assessing the "marketing relevance" of extracted topics by matching them against a configurable marketing keyword list/ontology
- so that the system can prioritize or flag topics that are more pertinent to marketers, and lay the groundwork for potential secondary focused searches (post-MVP).

## Acceptance Criteria (ACs)

1. A configurable list/ontology of marketing-related keywords and phrases is defined (e.g., in `core/config.py` or a separate JSON/YAML file).
2. A function is implemented in the `nlp_processing` module that takes the list of extracted topics (from Story 3.2) as input.
3. This function compares the extracted topics against the configured marketing keyword list/ontology.
4. The function flags topics that are considered "marketing-relevant" or assigns a relevance score. For MVP, a simple boolean flag (relevant/not relevant) or a count of matched keywords per topic is sufficient.
5. The marketing relevance assessment (e.g., list of matched keywords, or a relevance flag/score) is stored in the `ProcessedArticleDataModel` (e.g., in a `marketing_keywords_matched` JSON field or a `is_marketing_relevant` boolean field).
6. The design of this component considers future extension for triggering secondary, focused searches based on highly relevant topics (as per PRD FR1.5 - design for MVP, implementation post-MVP). This means the output should be structured in a way that these relevant topics can be easily identified.
7. Unit tests are implemented to verify the relevance assessment logic with sample topics and a mock marketing keyword list.

## Tasks / Subtasks

- [ ] Task 1: Define Marketing Keyword List/Ontology (AC: #1)
  - [ ] In `backend/app//core/config.py` (or a new `marketing_ontology.py` or JSON file loaded by config):
    - [ ] Define `MARKETING_KEYWORD_ONTOLOGY: List[str]` (or a more complex structure if doing more than keyword matching, e.g., Dict[str, List[str]] for categories). For MVP, a list of keywords/phrases is sufficient.
    - [ ] Populate with initial marketing-related terms (e.g., "content marketing", "seo", "social media advertising", "email campaign", "brand strategy", "influencer marketing", "customer engagement", "digital analytics", "conversion rate optimization").
  - [ ] Ensure this list is accessible via `core.config.settings`.
- [ ] Task 2: Implement Marketing Relevance Assessment Service (AC: #2, #3, #4)
  - [ ] Create `backend/app//nlp_processing/relevance_assessment_service.py`.
  - [ ] Implement `def assess_marketing_relevance(topics: List[str], marketing_keywords: List[str]) -> Dict[str, bool]:` (or returns a list of relevant topics, or a dict with scores).
    - [ ] For each topic in the input `topics` list:
      - [ ] Check if the topic (or its sub-phrases/keywords) matches any term in the `marketing_keywords` list.
      - [ ] Matching can be simple exact string matching (case-insensitive) or more flexible (e.g., checking if a keyword is a substring of a topic, or vice-versa). For MVP, case-insensitive substring matching is a good start.
    - [ ] Return a dictionary where keys are input topics and values are booleans indicating relevance (or a list of only relevant topics).
- [ ] Task 3: Integrate Relevance Storage into Data Processing Flow (AC: #5, #6)
  - [ ] Update `ProcessedArticleDataModel` in `backend/app//db/models_db.py` to include `marketing_keywords_matched = Column(JSON, nullable=True)` (to store a list of matched keywords or relevant topics).

        ```python
        # backend/app//db/models_db.py
        # class ProcessedArticleDataModel(Base):
        #    # ... other fields
        #    marketing_keywords_matched = Column(JSON, nullable=True) # Stores List[str] of matched keywords or relevant topics
        ```

  - [ ] In `nlp_processing/nlp_service.py`'s `process_article` method:
    - [ ] After topic extraction, call `relevance_assessment_service.assess_marketing_relevance(extracted_topics, settings.MARKETING_KEYWORD_ONTOLOGY)`.
    - [ ] Store the result (e.g., list of relevant topics/matched keywords) in the `marketing_keywords_matched` field of the `ProcessedArticleDataModel`.
    - [ ] Update the save operation for `ProcessedArticleDataModel`.
- [ ] Task 4: Implement Unit Tests (AC: #7)
  - [ ] Create `backend/tests/unit/nlp_processing/test_relevance_assessment_service.py`.
  - [ ] Test `assess_marketing_relevance`:
    - [ ] Provide sample lists of extracted topics and a sample marketing keyword list.
    - [ ] Verify it correctly identifies and flags/returns relevant topics based on various matching scenarios (exact match, partial match, case insensitivity).
    - [ ] Test with no matching topics.
  - [ ] Update tests for `nlp_service.process_article` to verify it calls the relevance service and stores the assessment correctly.

## Dev Technical Guidance

- **Marketing Keyword Ontology:** Start with a modest but representative list of keywords. This list is a key configuration point that will likely evolve. Consider making it easily updatable without code changes if possible (e.g., loading from a simple text or JSON file referenced in config).
- **Matching Logic:** For MVP, simple case-insensitive substring matching should be sufficient. For example, if "content marketing strategy" is a topic and "content marketing" is a keyword, it should match.
- **Output Structure for Relevance (AC #6):** Storing a list of the *actual matched marketing keywords* or the *input topics that were deemed relevant* in `marketing_keywords_matched` would be useful. This allows the Trend Identification Algorithm (Story 3.5) to directly use these relevant items and supports the design for future secondary searches (FR1.5).
- **Efficiency:** If the keyword list or topic list is very large, optimize the matching logic. For MVP scales (e.g., <100 keywords, <20 topics per article), nested loops with string checks are likely fine.
- **Configuration:** The marketing keyword list should be loaded via `core.config.settings`.

## Story Progress Notes

### Completion Notes List

### Change Log

- 2025-05-17 - Kayvan Sylvan - Initial draft
