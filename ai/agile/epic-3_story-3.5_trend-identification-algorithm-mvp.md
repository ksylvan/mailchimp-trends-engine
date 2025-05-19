# Story 3.5: Trend Identification Algorithm (Frequency & Growth Rate - MVP)

## Status: Draft

## Story

- As a Backend Developer Agent
- I want to implement an initial trend identification algorithm based on the frequency and basic growth rate of marketing-relevant topics
- so that the system can identify and score potential marketing trends from the processed article data.

## Acceptance Criteria (ACs)

1. A service or function aggregates marketing-relevant topic data from `ProcessedArticleDataModel` records (using topics identified as relevant in Story 3.4 and their associated `Workspaceed_at` timestamps from `RawArticleModel`).
2. The algorithm calculates the frequency of each marketing-relevant topic over defined time windows (e.g., daily, weekly counts - for MVP, daily might be too granular if data is sparse; consider a rolling window or comparing recent period vs. past period).
3. A basic growth rate or change in frequency for each marketing-relevant topic is computed (e.g., comparing current period's frequency to a previous period's frequency).
4. A "trend score" is calculated for each marketing-relevant topic based on a combination of its recent frequency and growth rate. The scoring logic should be simple for MVP but allow for future refinement.
5. Identified trends (e.g., the topic string, its calculated score, latest sentiment associated with articles mentioning it) are stored persistently using the `MarketingTrendModel` and `TrendDataPointModel` (as defined in `architecture.md`).
6. Unit tests are implemented with mock historical processed data to verify the trend identification algorithm's logic (frequency calculation, growth rate, scoring, and storage).
7. The trend identification process can be triggered (e.g., periodically after NLP processing, or via a manual API for MVP).

## Tasks / Subtasks

- [ ] Task 1: Define Trend Calculation Time Windows and Logic (AC: #2, #3, #4)
  - [ ] Decide on time window for frequency calculation (e.g., past 7 days vs. previous 7 days, or a simpler "current batch vs. historical average"). For MVP, a simple approach: consider all "recent" `ProcessedArticleDataModel` entries (e.g., last X days, configurable) for "current" frequency, and older ones for "past" frequency.
  - [ ] Define a simple scoring formula. Example: `trend_score = (current_frequency * weight_freq) + (growth_factor * weight_growth)`. `growth_factor` could be `(current_freq - past_freq) / past_freq` or simpler if `past_freq` is 0. Keep weights configurable.
- [ ] Task 2: Implement Trend Aggregation and Calculation Service (AC: #1, #2, #3, #4)
  - [ ] Create `backend/src/mailchimp_trends/trend_identification/trend_service.py`.
  - [ ] Implement `async def identify_and_score_trends(db: AsyncSession) -> List[MarketingTrendModel]:`.
    - [ ] Fetch `ProcessedArticleDataModel` records. Focus on those with `marketing_keywords_matched` (relevant topics from Story 3.4).
    - [ ] For each unique relevant topic:
      - [ ] Aggregate its occurrences over time using `raw_article.fetched_at`.
      - [ ] Calculate current frequency and past frequency based on defined time windows.
      - [ ] Calculate growth rate/factor.
      - [ ] Calculate the trend score.
      - [ ] Retrieve an overall sentiment for the topic (e.g., average or most recent sentiment from articles where this topic appeared and was deemed relevant). This might require joining `ProcessedArticleDataModel` with `RawArticleModel` to get `Workspaceed_at` and then looking up the `overall_sentiment` from `ProcessedArticleDataModel`.
    - [ ] Filter for topics that meet a minimum score or growth threshold to be considered a "trend".
    - [ ] Prepare data for storage.
- [ ] Task 3: Implement Trend Storage (AC: #5)
  - [ ] In `trend_service.py`, after identifying and scoring trends:
    - [ ] For each qualifying trend:
      - [ ] Check if a `MarketingTrendModel` for this topic name already exists.
      - [ ] If yes, update its `trend_score`, `current_sentiment`, and `last_updated_at`.
      - [ ] If no, create a new `MarketingTrendModel` instance.
      - [ ] Save the `MarketingTrendModel` (create or update).
      - [ ] Create a new `TrendDataPointModel` record for the current date/period, storing the `trend_id`, `datapoint_date` (current date), `score_at_date` (the new trend score), and `mention_frequency_at_date` (current frequency). Link it to the parent `MarketingTrendModel`.
      - [ ] Save the `TrendDataPointModel`.
- [ ] Task 4: Implement Trigger for Trend Identification (AC: #7)
  - [ ] In `nlp_processing/nlp_service.py` (or a new orchestration service):
    - [ ] After a batch of articles are processed by NLP, trigger `trend_service.identify_and_score_trends(db)`.
  - [ ] OR, create a manual API endpoint (similar to Story 2.2) `api/v1/admin/trigger-trend-identification` that calls this service. *Prefer this manual trigger for MVP control.*
- [ ] Task 5: Implement Unit Tests (AC: #6)
  - [ ] Create `backend/tests/unit/trend_identification/test_trend_service.py`.
  - [ ] Prepare mock `ProcessedArticleDataModel` data with varying topics, marketing relevance, and timestamps.
  - [ ] Test the aggregation logic (correctly counting frequencies in time windows).
  - [ ] Test the growth rate calculation.
  - [ ] Test the scoring formula with different inputs.
  - [ ] Test the logic for creating new `MarketingTrendModel` and `TrendDataPointModel` entries.
  - [ ] Test the logic for updating existing `MarketingTrendModel` entries and adding new `TrendDataPointModel` entries.
  - [ ] Mock database interactions to verify correct data is being saved.

## Dev Technical Guidance

- **Data Source for Trend ID:** The primary input will be `ProcessedArticleDataModel` records. Specifically, the `topics` (from Story 3.2) and `marketing_keywords_matched` (from Story 3.4) fields, along with the `raw_article.fetched_at` timestamp (requiring a join or access to the related `RawArticleModel`). Only topics identified as marketing-relevant should be considered for trend calculation.
- **Time Windows:**
  - Keep it simple for MVP. Perhaps:
    - "Current Period": articles fetched in the last 3-7 days.
    - "Previous Period": articles fetched in the 7 days prior to the current period.
  - These durations should be configurable (e.g., in `core/config.py`).
- **Growth Rate:** If `past_frequency` is 0, handle division by zero. A large growth factor can be assigned, or if `current_frequency` is also low, it might not be a strong trend.
- **Scoring Formula:** The example `trend_score = (current_frequency * weight_freq) + (growth_factor * weight_growth)` is a starting point. Weights should be configurable. Normalize scores if needed (e.g., to a 0-100 scale).
- **Sentiment for Trend:** A trend's sentiment could be the most recent sentiment of an article where the relevant topic appeared, or an average. For MVP, the sentiment of the latest processed article contributing to the trend might be simplest.
- **Database Models:** Ensure `MarketingTrendModel` and `TrendDataPointModel` from `architecture.md` are correctly implemented and used. `MarketingTrendModel` could store the topic name, current overall score, latest sentiment. `TrendDataPointModel` stores score/frequency snapshots over time.
- **Thresholds:** Implement configurable thresholds (e.g., minimum score, minimum frequency change) to decide if a scored topic qualifies as an actual "trend" to be displayed.

## Story Progress Notes

### Completion Notes List

{Any notes about implementation choices, difficulties, or follow-up needed}

### Change Log

- 2025-05-17 - Kayvan Sylvan - Initial draft
