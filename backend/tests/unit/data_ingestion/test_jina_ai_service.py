"Unit tests for Jina AI service integration."

import urllib.parse
from unittest.mock import AsyncMock, MagicMock

import httpx
import pytest
from _pytest.logging import LogCaptureFixture
from pytest_mock import MockerFixture

# Corrected import path based on project structure
from backend.app.data_ingestion.jina_ai_service import (
    DEFAULT_TIMEOUT,
    JINA_READER_BASE_URL,
    USER_AGENT,
    fetch_article_content,
)


@pytest.mark.asyncio
async def test_fetch_article_content_success(mocker: MockerFixture):
    """
    Tests successful content fetching from Jina AI Reader.
    """
    _ = mocker

    mock_url = "http://example.com/article"
    mock_encoded_url = urllib.parse.quote(mock_url, safe="")
    expected_jina_url = f"{JINA_READER_BASE_URL}{mock_encoded_url}"
    mock_article_text = "This is a mock article content."

    mock_response = MagicMock(spec=httpx.Response)
    mock_response.status_code = 200
    mock_response.text = mock_article_text
    mock_response.raise_for_status = MagicMock()

    mock_async_client = AsyncMock(spec=httpx.AsyncClient)
    mock_async_client.get = AsyncMock(return_value=mock_response)

    content = await fetch_article_content(mock_url, mock_async_client)

    assert content == mock_article_text
    mock_async_client.get.assert_called_once_with(
        expected_jina_url,
        headers={"Accept": "text/plain", "User-Agent": USER_AGENT},
        timeout=DEFAULT_TIMEOUT,
    )
    mock_response.raise_for_status.assert_called_once()


@pytest.mark.asyncio
async def test_fetch_article_content_http_error(
    mocker: MockerFixture, caplog: LogCaptureFixture
):
    """
    Tests handling of HTTPStatusError from Jina AI Reader.
    """
    _ = mocker
    mock_url = "http://example.com/notfound"
    mock_encoded_url = urllib.parse.quote(mock_url, safe="")
    expected_jina_url = f"{JINA_READER_BASE_URL}{mock_encoded_url}"

    # Mock the request object that would be part of HTTPStatusError
    mock_request = MagicMock(spec=httpx.Request)
    mock_request.url = expected_jina_url

    # Mock the response object that would be part of HTTPStatusError
    mock_error_response = MagicMock(spec=httpx.Response)
    mock_error_response.status_code = 404
    mock_error_response.text = "Not Found"

    http_status_error = httpx.HTTPStatusError(
        message="404 Client Error: Not Found for url",
        request=mock_request,
        response=mock_error_response,
    )

    mock_async_client = AsyncMock(spec=httpx.AsyncClient)
    # Config mock .get() to raise HTTPStatusError.
    # The actual response.raise_for_status() is what throws the error.
    # So, .get() returns a response, and that response's .raise_for_status() throws.
    mock_response_that_will_fail = MagicMock(spec=httpx.Response)
    mock_response_that_will_fail.status_code = 404
    mock_response_that_will_fail.text = "Simulated Not Found"
    mock_response_that_will_fail.request = mock_request  # Attach request to response
    mock_response_that_will_fail.raise_for_status = MagicMock(
        side_effect=http_status_error
    )

    mock_async_client.get = AsyncMock(return_value=mock_response_that_will_fail)

    caplog.clear()  # Clear any previous logs
    content = await fetch_article_content(mock_url, mock_async_client)

    assert content is None
    mock_async_client.get.assert_called_once_with(
        expected_jina_url,
        headers={"Accept": "text/plain", "User-Agent": USER_AGENT},
        timeout=DEFAULT_TIMEOUT,
    )
    # Ensure raise_for_status was called on the response object returned by client.get()
    mock_response_that_will_fail.raise_for_status.assert_called_once()

    assert f"HTTP error occurred when fetching {mock_url} via Jina" in caplog.text
    assert "Status 404" in caplog.text


@pytest.mark.asyncio
async def test_fetch_article_content_request_error(
    mocker: MockerFixture, caplog: LogCaptureFixture
):
    """
    Tests handling of RequestError (e.g., network issue) from Jina AI Reader.
    """
    _ = mocker
    mock_url = "http://example.com/networkissue"
    mock_encoded_url = urllib.parse.quote(mock_url, safe="")
    expected_jina_url = f"{JINA_READER_BASE_URL}{mock_encoded_url}"

    # Mock the request object that would be part of RequestError
    mock_request = MagicMock(spec=httpx.Request)
    mock_request.url = expected_jina_url

    request_error = httpx.RequestError(message="Network timeout", request=mock_request)

    mock_async_client = AsyncMock(spec=httpx.AsyncClient)
    mock_async_client.get = AsyncMock(side_effect=request_error)

    caplog.clear()
    content = await fetch_article_content(mock_url, mock_async_client)

    assert content is None
    mock_async_client.get.assert_called_once_with(
        expected_jina_url,
        headers={"Accept": "text/plain", "User-Agent": USER_AGENT},
        timeout=DEFAULT_TIMEOUT,
    )
    assert f"Request error occurred when fetching {mock_url} via Jina" in caplog.text
    assert "RequestError" in caplog.text  # Check for the class name of the error


@pytest.mark.asyncio
async def test_fetch_article_content_empty_url(
    mocker: MockerFixture, caplog: LogCaptureFixture
):
    """
    Tests behavior when an empty URL is provided.
    """
    _ = mocker
    mock_async_client = AsyncMock(spec=httpx.AsyncClient)

    caplog.clear()
    content = await fetch_article_content("", mock_async_client)

    assert content is None
    mock_async_client.get.assert_not_called()  # Should not attempt to fetch
    assert "fetch_article_content called with empty URL" in caplog.text


@pytest.mark.asyncio
async def test_fetch_article_content_unexpected_error(
    mocker: MockerFixture, caplog: LogCaptureFixture
):
    """
    Tests handling of unexpected errors during Jina AI Reader call.
    """
    _ = mocker
    mock_url = "http://example.com/unexpected"
    mock_encoded_url = urllib.parse.quote(mock_url, safe="")
    expected_jina_url = f"{JINA_READER_BASE_URL}{mock_encoded_url}"

    unexpected_error = Exception("Something totally unexpected happened")

    mock_async_client = AsyncMock(spec=httpx.AsyncClient)
    mock_async_client.get = AsyncMock(side_effect=unexpected_error)

    caplog.clear()
    content = await fetch_article_content(mock_url, mock_async_client)

    assert content is None
    mock_async_client.get.assert_called_once_with(
        expected_jina_url,
        headers={"Accept": "text/plain", "User-Agent": USER_AGENT},
        timeout=DEFAULT_TIMEOUT,
    )
    assert (
        f"A truly unexpected error occurred when fetching {mock_url} via Jina."
    ) in caplog.text
    assert "Something totally unexpected happened" in caplog.text
