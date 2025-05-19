"""Test server module for FastAPI application."""

from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient

from backend.app.__about__ import __version__ as expected_app_version
from backend.app.server import app, lifespan

# backend/tests/test_server.py

# Relative imports based on the file structure:
# tests/test_server.py will import from app/server.py and app/__about__.py


@pytest.fixture(scope="module", name="client")
def client_fixture() -> Iterator[TestClient]:
    """
    Pytest fixture to create a TestClient for the FastAPI application.
    The client is created once per module and handles startup/shutdown via
    context manager.
    """
    with TestClient(app) as test_client:
        yield test_client


def test_health_check(client: TestClient):
    """
    Test the /health endpoint.
    Ensures it returns a 200 OK status and the correct JSON response.
    """
    response = client.get("/health")
    assert response.status_code == 200
    # app.version is initialized from __version__ in server.py
    # This test verifies the endpoint returns that version correctly.
    assert response.json() == {"status": "ok", "version": app.version}


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
    # FastAPI stores the lifespan context manager at app.router.lifespan_context
    assert app.router.lifespan_context is lifespan
