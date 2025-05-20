"""Unit tests for the /health endpoint."""

from fastapi.testclient import TestClient

from backend.app.__about__ import __version__ as app_version
from backend.app.server import app  # Import your FastAPI app instance

client = TestClient(app)


def test_health_check_returns_200_ok():
    """Test that the /health endpoint returns a 200 OK status."""
    response = client.get("/health")
    assert response.status_code == 200


def test_health_check_returns_correct_payload():
    """Test that the /health endpoint returns the correct status and version."""
    response = client.get("/health")
    expected_payload = {"status": "healthy", "version": app_version}
    assert response.json() == expected_payload

    payload_version = response.json().get("version")
    # Double check the version from __about__ directly for this test
    assert app_version == payload_version, (
        f"App version mismatch: expected {app_version}, got {payload_version}"
    )
