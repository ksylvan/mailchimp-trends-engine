# Story 2.3: Raw Content Storage (Preliminary)

## Status: Draft

## Story

- As a Backend Developer Agent
- I want to implement a preliminary storage mechanism for the raw article text and basic metadata fetched by the Jina AI Reader service
- so that this content is persisted and can be retrieved by the NLP processing module.

## Acceptance Criteria (ACs)

1. A clear interface or set of functions is defined for the NLP module to retrieve raw article content for processing.
2. The system stores the full extracted textual content (from Jina AI Reader) and basic metadata (source URL, fetch timestamp) for each fetched article.
3. For the MVP, storage can be simple files on a Docker volume, with uniquely named files (e.g., based on a hash of the URL or a UUID, plus timestamp) to organize content. (Database storage via SQLAlchemy models is the actual target as per `architecture.md` - this story will implement that).
4. The storage mechanism includes a basic check to avoid re-processing/re-storing identical content if fetched again (e.g., based on source URL if content is assumed static for a given URL, or a hash of the content if URLs might serve dynamic content frequently). For MVP, checking by source URL is sufficient.
5. SQLAlchemy models (`RawArticleModel`) are used to interact with the SQLite database as defined in `architecture.md`.
6. The `perform_scheduled_article_fetch` function (from Story 2.2) is updated to use this storage mechanism to save fetched content.
7. Unit tests are implemented to verify the storage and retrieval logic, including the check for duplicate content (by source URL).

## Tasks / Subtasks

- [ ] Task 1: Define/Refine SQLAlchemy Model for Raw Articles (AC: #5)
  - [ ] Review `RawArticleModel` in `backend/src/mailchimp_trends/db/models_db.py` (as defined in `architecture.md`). Ensure it includes fields for `id` (PK), `source_url` (unique), `content_text`, and `Workspaceed_at`.

        ```python
        # backend/src/mailchimp_trends/db/models_db.py
        # class RawArticleModel(Base):
        #     __tablename__ = "raw_articles"
        #     id = Column(Integer, primary_key=True, index=True, autoincrement=True)
        #     source_url = Column(String, unique=True, index=True, nullable=False)
        #     content_text = Column(Text, nullable=False)
        #     fetched_at = Column(DateTime, default=datetime.utcnow, nullable=False)
        ```

  - [ ] Ensure the database schema is created/updated if `main.py` or a startup script runs `Base.metadata.create_all(bind=engine)`.
- [ ] Task 2: Create Raw Content Storage Service/Functions (AC: #1, #2, #4)
  - [ ] Create `backend/src/mailchimp_trends/data_ingestion/content_store_service.py`.
  - [ ] Implement `async def save_raw_article(db: AsyncSession, source_url: str, content_text: str) -> RawArticleModel | None:`
    - [ ] Check if an article with the `source_url` already exists in the database.
      - [ ] If yes, log that content for this URL already exists and optionally update `Workspaceed_at` or return the existing record. (For MVP, simply skip re-inserting and log).
    - [ ] If no, create a new `RawArticleModel` instance with the provided data.
    - [ ] Add the new instance to the session and commit: `db.add(new_article); await db.commit(); await db.refresh(new_article)`.
    - [ ] Return the saved `RawArticleModel` instance. Handle potential database errors (e.g., `IntegrityError` if somehow a duplicate URL slips through, though the initial check should prevent this).
  - [ ] Implement `async def get_raw_article_by_url(db: AsyncSession, source_url: str) -> RawArticleModel | None:` (for testing/verification).
  - [ ] Implement `async def get_unprocessed_articles(db: AsyncSession, limit: int = 10) -> List[RawArticleModel]:` (AC #1 - placeholder for NLP module, actual criteria for "unprocessed" might be refined in NLP stories, e.g., by checking for linked processed data). For now, it can just fetch recent articles.
- [ ] Task 3: Integrate Storage into Fetching Process (AC: #6)
  - [ ] Modify `perform_scheduled_article_fetch` in `backend/src/mailchimp_trends/data_ingestion/scheduler.py` (or wherever it was defined in Story 2.2).
  - [ ] Inject `AsyncSession` (FastAPI dependency injection) into this function or ensure it can access one.
  - [ ] After `jina_ai_service.fetch_article_content(url)` successfully returns content:
    - [ ] Call `save_raw_article(db=db, source_url=url, content_text=fetched_content)`.
    - [ ] Log success or failure of the save operation.
- [ ] Task 4: Implement Unit Tests for Content Storage Service (AC: #7)
  - [ ] Create `backend/tests/unit/data_ingestion/test_content_store_service.py`.
  - [ ] Use an in-memory SQLite database for these tests or a test-specific file DB.
  - [ ] **Test Case 1 (Save New Article):**
    - [ ] Call `save_raw_article` with new data.
    - [ ] Assert a `RawArticleModel` instance is returned and data matches.
    - [ ] Verify the article exists in the DB.
  - [ ] **Test Case 2 (Attempt to Save Duplicate URL):**
    - [ ] Call `save_raw_article` once.
    - [ ] Call `save_raw_article` again with the same `source_url`.
    - [ ] Assert that a new record is NOT created (or that the existing one is appropriately handled as per design - e.g., timestamp updated, or simply skipped). Verify logging.
  - [ ] **Test Case 3 (Retrieve Article):**
    - [ ] Test `get_raw_article_by_url` and `get_unprocessed_articles` for basic functionality.

## Dev Technical Guidance

- **SQLAlchemy Session Management:** Use FastAPI's dependency injection for `AsyncSession`. Define a dependency like:

        ```python
        # backend/src/mailchimp_trends/db/session.py (example)
        from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
        from sqlalchemy.orm import sessionmaker
        from mailchimp_trends.core.config import settings # Assuming DB URL is in settings

        engine = create_async_engine(settings.ASYNC_DATABASE_URL) # e.g., "sqlite+aiosqlite:///./mailchimp_trends.db"
        AsyncSessionFactory = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

        async def get_db_session() -> AsyncSession:
            async with AsyncSessionFactory() as session:
                yield session
        ```

    Then use `db: AsyncSession = Depends(get_db_session)` in service functions or API routes that need DB access.
- **Unique Constraint:** The `source_url = Column(String, unique=True, index=True)` in `RawArticleModel` will enforce uniqueness at the DB level. The service logic should gracefully handle or preempt `IntegrityError` from SQLAlchemy.
- **"Unprocessed" Logic:** The initial `get_unprocessed_articles` can be simple (e.g., fetch articles ORDER BY `Workspaceed_at` DESC). Later, when `ProcessedArticleDataModel` is introduced (Epic 3), this function will be refined to select articles that don't yet have corresponding entries in the processed data table.
- **Avoiding Re-processing (AC #4):** The check `if an article with the source_url already exists` in `save_raw_article` handles this for MVP. More sophisticated content hashing could be added post-MVP if URLs serve frequently changing content that still needs to be captured if truly different.
- **Error Handling:** Ensure database operations are within `try-except` blocks to catch potential exceptions like `SQLAlchemyError`.

## Story Progress Notes

### Completion Notes List

{Any notes about implementation choices, difficulties, or follow-up needed}

### Change Log

2025-05-17 - Kayvan Sylvan - Initial draft
