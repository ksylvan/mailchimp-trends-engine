"""Unit tests for the scheduler module functionality."""

import logging
from unittest.mock import MagicMock, patch

import pytest
from pytest import LogCaptureFixture

from backend.app.data_ingestion.scheduler import shutdown_scheduler, start_scheduler

pytestmark = pytest.mark.asyncio


async def test_start_scheduler_when_not_running():
    """Test starting the scheduler when it's not already running."""
    # Create a mock scheduler
    mock_scheduler = MagicMock()
    mock_scheduler.running = False

    # Patch the scheduler reference in the module
    with patch("backend.app.data_ingestion.scheduler.scheduler", mock_scheduler):
        await start_scheduler()
        mock_scheduler.start.assert_called_once()


async def test_start_scheduler_when_already_running(caplog: LogCaptureFixture):
    """Test starting the scheduler when it's already running."""
    # Set the appropriate log level to capture INFO logs
    caplog.set_level(logging.INFO)

    # Create a mock scheduler
    mock_scheduler = MagicMock()
    mock_scheduler.running = True

    # Patch the scheduler reference in the module
    with patch("backend.app.data_ingestion.scheduler.scheduler", mock_scheduler):
        await start_scheduler()

        # Verify that start() wasn't called
        mock_scheduler.start.assert_not_called()

        # Verify the log message was generated
        assert any(
            "Scheduler is already running" in rec.message for rec in caplog.records
        )


async def test_shutdown_scheduler_when_running():
    """Test shutting down the scheduler when it's running."""
    # Create a mock scheduler
    mock_scheduler = MagicMock()
    mock_scheduler.running = True

    # Patch the scheduler reference in the module
    with patch("backend.app.data_ingestion.scheduler.scheduler", mock_scheduler):
        await shutdown_scheduler()
        mock_scheduler.shutdown.assert_called_once_with(wait=False)


async def test_shutdown_scheduler_when_not_running(caplog: LogCaptureFixture):
    """Test shutting down the scheduler when it's not running."""
    # Set the appropriate log level to capture INFO logs
    caplog.set_level(logging.INFO)

    # Create a mock scheduler
    mock_scheduler = MagicMock()
    mock_scheduler.running = False

    # Patch the scheduler reference in the module
    with patch("backend.app.data_ingestion.scheduler.scheduler", mock_scheduler):
        await shutdown_scheduler()

        # Verify that shutdown() wasn't called
        mock_scheduler.shutdown.assert_not_called()

        # Verify the log message was generated
        assert any("Scheduler is not running" in rec.message for rec in caplog.records)
