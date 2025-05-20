"""Unit tests for the data ingestion API router."""

import logging
from unittest.mock import AsyncMock, patch

from fastapi import status
from fastapi.testclient import TestClient

from backend.app.server import app

client = TestClient(app)


def test_trigger_fetch_success():
    """Test /api/v1/data-ingestion/trigger-fetch endpoint returns 202 on success."""
    with patch(
        "backend.app.api.v1.routers.data_ingestion.perform_scheduled_article_fetch",
        new_callable=AsyncMock,
    ):
        response = client.post("/api/v1/data-ingestion/trigger-fetch")
        assert response.status_code == status.HTTP_202_ACCEPTED
        assert response.json() == {
            "message": "Article fetching job has been scheduled successfully."
        }


def test_trigger_fetch_error():
    """
    Test that the /api/v1/data-ingestion/trigger-fetch endpoint
    returns 500 when an exception occurs before scheduling the background task.
    """
    # Mock BackgroundTasks.add_task to raise an exception directly
    with patch(
        "fastapi.BackgroundTasks.add_task",
        side_effect=Exception("Test error"),
    ):
        # Disable the logging for cleaner test output
        logging.disable(logging.ERROR)
        try:
            response = client.post("/api/v1/data-ingestion/trigger-fetch")
            assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
            assert (
                "Failed to schedule article fetching job" in response.json()["detail"]
            )
        finally:
            # Re-enable logging
            logging.disable(logging.NOTSET)
