"""Unit tests for the server.main() function, mocking uvicorn."""

from unittest import mock

from backend.app import server as server_mod


@mock.patch("backend.app.server.uvicorn.run")
def test_main_happy_path(mock_uvicorn_run: mock.Mock):
    """
    Test that server.main() calls uvicorn.run with correct defaults.
    """
    server_mod.main()
    mock_uvicorn_run.assert_called_once()
    args, kwargs = mock_uvicorn_run.call_args
    # The first arg is the app, which should be server_mod.app
    assert args[0] is server_mod.app
    assert kwargs["host"] == "0.0.0.0"
    assert kwargs["port"] == 8000
    assert kwargs["log_level"] == "info"


# Additional test for log_level argument
@mock.patch("backend.app.server.uvicorn.run")
def test_main_custom_log_level(mock_uvicorn_run: mock.Mock):
    """
    Test that server.main() passes a custom log_level to uvicorn.run.
    """
    server_mod.main(log_level="debug")
    mock_uvicorn_run.assert_called_once()
    _, kwargs = mock_uvicorn_run.call_args
    assert kwargs["log_level"] == "debug"


# Test: main() should call uvicorn.run even if log_level is uppercase
@mock.patch("backend.app.server.uvicorn.run")
def test_main_log_level_case_insensitive(mock_uvicorn_run: mock.Mock):
    """
    Test that server.main() passes uppercase log_level to uvicorn.run.
    """
    server_mod.main(log_level="WARNING")
    mock_uvicorn_run.assert_called_once()
    _, kwargs = mock_uvicorn_run.call_args
    assert kwargs["log_level"] == "WARNING"
