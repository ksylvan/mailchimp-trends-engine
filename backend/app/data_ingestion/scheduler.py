"""
Scheduler for periodically fetching articles.

This module sets up and manages scheduled tasks for data ingestion,
primarily for fetching new articles from configured news sources.
It uses APScheduler for scheduling and integrates with the Jina AI service
for content fetching.
"""

import asyncio
import logging

import httpx  # Third-party import
from apscheduler.schedulers.asyncio import AsyncIOScheduler  # type: ignore

from backend.app.core.config import settings  # First-party import
from backend.app.data_ingestion.jina_ai_service import (
    fetch_article_content,  # First-party import
)

logger = logging.getLogger(__name__)

scheduler = AsyncIOScheduler()

PROCESSING_DELAY_SECONDS = 0.1


# Placeholder for actual content processing/storage (Story 2.3)
async def process_fetched_content(url: str, content: str):
    """Placeholder function to process fetched content."""
    logger.info(
        "Placeholder: Processing content from %s. Length: %s", url, len(content)
    )
    # In Story 2.3, this will involve saving to the database.
    await asyncio.sleep(PROCESSING_DELAY_SECONDS)  # Simulate processing delay


async def perform_scheduled_article_fetch():
    """
    Fetches articles from configured news sources.
    This job is intended to be scheduled.
    """
    logger.info("Starting scheduled article fetch cycle...")
    source_count = 0
    fetched_count = 0

    async with httpx.AsyncClient() as client:
        for url in settings.NEWS_SOURCES:
            source_count += 1
            logger.info("Fetching content from URL: %s", url)
            try:
                content = await fetch_article_content(url, client=client)
                if content:
                    logger.info(
                        "Successfully fetched content from %s. Length: %s",
                        url,
                        len(content),
                    )
                    # For MVP, log a snippet. Actual storage in Story 2.3
                    # logger.debug("Content snippet for %s: %s", url, content[:200])
                    await process_fetched_content(url, content)
                    fetched_count += 1
                else:
                    # Error logging is handled within fetch_article_content
                    logger.warning("No content fetched for URL: %s", url)
            except Exception as e:  # noqa: BLE001 # pylint: disable=broad-except
                logger.error(
                    "Unhandled exception during processing of URL %s: %s", url, e
                )

            # Delay should happen after processing each URL (success or fail),
            # but not after the very last one.
            if source_count < len(settings.NEWS_SOURCES):
                logger.info(
                    "Waiting for %s seconds before next fetch...",
                    settings.JINA_FETCH_DELAY_SECONDS,
                )
                await asyncio.sleep(settings.JINA_FETCH_DELAY_SECONDS)

    logger.info(
        "Scheduled article fetch cycle completed. Fetched %s out of %s sources.",
        fetched_count,
        len(settings.NEWS_SOURCES),
    )


async def start_scheduler():
    """Starts the APScheduler."""
    if not scheduler.running:
        scheduler.start()
        logger.info("Scheduler started.")
    else:
        logger.info("Scheduler is already running.")


async def shutdown_scheduler():
    """Shuts down the APScheduler."""
    if scheduler.running:
        scheduler.shutdown(wait=False)
        logger.info("Scheduler shut down.")
    else:
        logger.info("Scheduler is not running.")
