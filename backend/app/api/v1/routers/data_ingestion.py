"""Data Ingestion API Router"""

import logging

from fastapi import APIRouter, BackgroundTasks, HTTPException, status

from backend.app.data_ingestion.scheduler import perform_scheduled_article_fetch

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post(
    "/trigger-fetch",
    summary="Manually trigger article fetching",
    status_code=status.HTTP_202_ACCEPTED,
)
async def trigger_fetch_articles(background_tasks: BackgroundTasks):
    """
    Manually triggers the scheduled article fetching job.
    This is useful for MVP demonstration purposes.
    """
    logger.info("Manual trigger received for article fetching.")
    try:
        # Running as a background task to avoid blocking the HTTP response.
        background_tasks.add_task(perform_scheduled_article_fetch)
        return {"message": "Article fetching job has been scheduled successfully."}
    except Exception as e:
        logger.error("Error scheduling article fetching job: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to schedule article fetching job: {str(e)}",
        ) from e
