"""Unit tests for basic application configuration and properties."""

import logging

import pytest
from fastapi.testclient import TestClient

from backend.app.__about__ import __version__ as expected_app_version
from backend.app.server import app


def test_app_version_matches_about_version():
    """
    Test that the application's version (app.version) is correctly
    set from the __version__ variable in __about__.py.
    """
    assert app.version == expected_app_version


def test_lifespan_is_configured():
    """
    Test that the custom lifespan event handler is correctly configured
    on the FastAPI application instance.
    """
    # Check that a lifespan context is configured on the router.
    # FastAPI wraps the lifespan, so direct identity check is brittle.
    assert app.router.lifespan_context is not None


def test_lifespan_logs_startup_and_shutdown(
    caplog: pytest.LogCaptureFixture,
):  # Removed client fixture
    """
    Test that the lifespan manager logs startup and shutdown messages.
    The 'caplog' fixture captures log output.
    A local TestClient is used to trigger lifespan events for this test.
    """

    # Get the logger instance used in app.server
    app_server_logger = logging.getLogger("backend.app.server")
    # Ensure its level is INFO so messages pass through to handlers/caplog
    original_level = app_server_logger.level
    app_server_logger.setLevel(logging.INFO)

    caplog.clear()

    try:
        with caplog.at_level(logging.INFO, logger="backend.app.server"):
            with (
                TestClient(app) as _local_client
            ):  # Indicate _local_client is not directly used after this
                # This will trigger startup logs for this specific client instance
                # and they should be captured by this test's caplog.
                startup_log_found = any(
                    "Application startup. Version: " in record.message
                    and record.levelname == "INFO"
                    for record in caplog.records
                )
                assert startup_log_found, (
                    "Startup log message not found in caplog.records"
                )

                version_log_found = any(
                    f"Version: {app.version}" in record.message
                    and record.levelname == "INFO"
                    for record in caplog.records
                )
                assert version_log_found, (
                    f"Version log message for {app.version} not found"
                )

                docs_log_found = any(
                    "API documentation available at /docs or /redoc" in record.message
                    and record.levelname == "INFO"
                    for record in caplog.records
                )
                assert docs_log_found, "Docs log message not found"

            # After the 'with' block, shutdown logs should be emitted by local_client
            # and still be within the caplog.at_level context.
            # We need to check records added *after* the startup ones.
            # A simple way is to check the last relevant record.
            shutdown_log_found = any(
                "Application shutdown." in record.message and record.levelname == "INFO"
                for record in caplog.records
            )
            assert shutdown_log_found, "Shutdown log message not found"

    finally:
        # Restore original logger level
        app_server_logger.setLevel(original_level)
