"Configure pytest to run with the backend module"

import os
import sys
from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient

# Add the project root to the Python path
# This ensures that 'from app import ...' or
# 'from backend.app import ...' works in tests
# Assumes conftest.py is in backend/tests/
project_root_for_backend = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)
if project_root_for_backend not in sys.path:
    sys.path.insert(0, project_root_for_backend)

project_root_top_level = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)
if project_root_top_level not in sys.path:
    sys.path.insert(0, project_root_top_level)


@pytest.fixture(scope="session")  # Changed scope to session for efficiency
def client() -> Iterator[TestClient]:
    """
    Pytest fixture to create a TestClient for the FastAPI application.
    The client is created once per test session and handles startup/shutdown.
    """

    from backend.app import server as b_a_s  # pylint: disable=import-outside-toplevel

    with TestClient(b_a_s.app) as test_client:
        yield test_client
