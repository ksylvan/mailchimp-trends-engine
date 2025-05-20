import logging

from app.data_ingestion.scheduler import perform_scheduled_article_fetch
from fastapi import APIRouter, HTTPException, status

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post(
    "/trigger-fetch",
    summary="Manually trigger article fetching",
    status_code=status.HTTP_202_ACCEPTED,
)
async def trigger_fetch_articles():
    """
    Manually triggers the scheduled article fetching job.
    This is useful for MVP demonstration purposes.
    """
    logger.info("Manual trigger received for article fetching.")
    try:
        # Running as a background task or directly awaiting.
        # For simplicity in MVP, await directly.
        # For production, consider background tasks:
        # background_tasks.add_task(perform_scheduled_article_fetch)
        await perform_scheduled_article_fetch()
        return {"message": "Article fetching job triggered successfully."}
    except Exception as e:
        logger.error("Error triggering article fetching job: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to trigger article fetching job: {str(e)}",
        ) from e
