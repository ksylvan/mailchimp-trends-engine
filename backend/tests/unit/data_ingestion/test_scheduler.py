"""Unit tests for the article fetching scheduler."""

import logging  # Added import
from unittest.mock import ANY, AsyncMock, patch  # Added ANY

import pytest
from app.data_ingestion.scheduler import perform_scheduled_article_fetch

# Mark all tests in this file as asyncio
pytestmark = pytest.mark.asyncio


@patch("app.data_ingestion.scheduler.fetch_article_content", new_callable=AsyncMock)
@patch("app.data_ingestion.scheduler.settings")
async def test_perform_scheduled_article_fetch_success(
    mock_settings_patch, mock_fetch_article_content, caplog
):
    """
    Tests successful execution of perform_scheduled_article_fetch.
    """
    mock_settings_patch.NEWS_SOURCES = [
        "http://example.com/news1",
        "http://example.com/news2",
    ]
    mock_settings_patch.JINA_FETCH_DELAY_SECONDS = 0.1  # Minimal delay for testing
    caplog.set_level(logging.INFO)  # Ensure INFO logs are captured BEFORE the call

    # Configure mock_fetch_article_content to return different content
    # for different URLs
    async def side_effect_fetch(
        url,
        client=None,  # pylint: disable=unused-argument
    ):  # Changed to client, added pylint disable
        if url == "http://example.com/news1":
            return "Content from news1"
        if url == "http://example.com/news2":
            return "Content from news2"
        return None

    mock_fetch_article_content.side_effect = side_effect_fetch

    with patch(
        "app.data_ingestion.scheduler.asyncio.sleep", new_callable=AsyncMock
    ) as mock_sleep:
        await perform_scheduled_article_fetch()

    assert mock_fetch_article_content.call_count == 2
    mock_fetch_article_content.assert_any_call("http://example.com/news1", client=ANY)
    mock_fetch_article_content.assert_any_call("http://example.com/news2", client=ANY)

    # Check if asyncio.sleep was called.
    # 2 calls from process_fetched_content (mocked as 0.1s sleep)
    # 1 call from the loop itself (JINA_FETCH_DELAY_SECONDS = 0.1s)
    assert mock_sleep.call_count == 3
    mock_sleep.assert_any_call(0.1)

    # caplog.set_level(logging.INFO) # Moved up
    assert "Starting scheduled article fetch cycle..." in caplog.text
    assert "Fetching content from URL: http://example.com/news1" in caplog.text
    assert (
        "Successfully fetched content from http://example.com/news1. Length: 18"
        in caplog.text
    )
    assert (
        "Placeholder: Processing content from http://example.com/news1. Length: 18"
        in caplog.text
    )
    assert "Fetching content from URL: http://example.com/news2" in caplog.text
    assert (
        "Successfully fetched content from http://example.com/news2. Length: 18"
        in caplog.text
    )
    assert (
        "Placeholder: Processing content from http://example.com/news2. Length: 18"
        in caplog.text
    )
    assert "Waiting for 0.1 seconds before next fetch..." in caplog.text
    assert (
        "Scheduled article fetch cycle completed. Fetched 2 out of 2 sources."
        in caplog.text
    )


@patch("app.data_ingestion.scheduler.fetch_article_content", new_callable=AsyncMock)
@patch("app.data_ingestion.scheduler.settings")
async def test_perform_scheduled_article_fetch_one_fails(
    mock_settings_patch, mock_fetch_article_content, caplog
):
    """
    Tests perform_scheduled_article_fetch when one article fetch fails.
    """
    mock_settings_patch.NEWS_SOURCES = [
        "http://example.com/news1",
        "http://example.com/news_fail",
    ]
    mock_settings_patch.JINA_FETCH_DELAY_SECONDS = 0.1
    caplog.set_level(logging.INFO)

    async def side_effect_fetch(
        url,
        client=None,  # pylint: disable=unused-argument
    ):  # Changed to client, added pylint disable
        if url == "http://example.com/news1":
            return "Content from news1"
        if url == "http://example.com/news_fail":
            # Simulate failure in fetch_article_content by returning None
            # Error logging for this specific failure is assumed to be in
            # fetch_article_content
            return None
        return None

    mock_fetch_article_content.side_effect = side_effect_fetch

    with patch(
        "app.data_ingestion.scheduler.asyncio.sleep", new_callable=AsyncMock
    ) as mock_sleep:
        await perform_scheduled_article_fetch()

    assert mock_fetch_article_content.call_count == 2
    # caplog.set_level(logging.INFO) # Moved up
    assert "Fetching content from URL: http://example.com/news_fail" in caplog.text
    assert "No content fetched for URL: http://example.com/news_fail" in caplog.text
    assert (
        "Scheduled article fetch cycle completed. Fetched 1 out of 2 sources."
        in caplog.text
    )
    assert mock_sleep.call_count == 2


@patch("app.data_ingestion.scheduler.fetch_article_content", new_callable=AsyncMock)
@patch("app.data_ingestion.scheduler.settings")
async def test_perform_scheduled_article_fetch_all_fail(
    mock_settings_patch, mock_fetch_article_content, caplog
):
    """
    Tests perform_scheduled_article_fetch when all article fetches fail.
    """
    mock_settings_patch.NEWS_SOURCES = [
        "http://example.com/news_fail1",
        "http://example.com/news_fail2",
    ]
    mock_settings_patch.JINA_FETCH_DELAY_SECONDS = 0.1
    mock_fetch_article_content.return_value = None  # All fetches fail
    caplog.set_level(logging.INFO)

    with patch(
        "app.data_ingestion.scheduler.asyncio.sleep", new_callable=AsyncMock
    ) as mock_sleep:
        await perform_scheduled_article_fetch()

    assert mock_fetch_article_content.call_count == 2
    # caplog.set_level(logging.INFO) # Moved up
    assert "No content fetched for URL: http://example.com/news_fail1" in caplog.text
    assert "No content fetched for URL: http://example.com/news_fail2" in caplog.text
    assert (
        "Scheduled article fetch cycle completed. Fetched 0 out of 2 sources."
        in caplog.text
    )
    assert mock_sleep.call_count == 1


@patch("app.data_ingestion.scheduler.fetch_article_content", new_callable=AsyncMock)
@patch("app.data_ingestion.scheduler.settings")
async def test_perform_scheduled_article_fetch_exception_during_fetch(
    mock_settings_patch, mock_fetch_article_content, caplog
):
    """
    Tests perform_scheduled_article_fetch when an unhandled exception occurs
    during a fetch_article_content call.
    """
    mock_settings_patch.NEWS_SOURCES = ["http://example.com/news_exception"]
    mock_settings_patch.JINA_FETCH_DELAY_SECONDS = 0.1
    mock_fetch_article_content.side_effect = Exception("Simulated network error")
    caplog.set_level(logging.INFO)

    # No need to mock sleep here as it won't be reached if
    # there's only one URL and it errors
    await perform_scheduled_article_fetch()

    assert mock_fetch_article_content.call_count == 1
    # caplog.set_level(logging.INFO) # Moved up
    assert "Fetching content from URL: http://example.com/news_exception" in caplog.text
    assert (
        "Unhandled exception during processing of URL "
        "http://example.com/news_exception: Simulated network error" in caplog.text
    )
    assert (
        "Scheduled article fetch cycle completed. Fetched 0 out of 1 sources."
        in caplog.text
    )


@patch("app.data_ingestion.scheduler.settings")
async def test_perform_scheduled_article_fetch_no_sources(mock_settings_patch, caplog):
    """
    Tests perform_scheduled_article_fetch with an empty list of news sources.
    """
    mock_settings_patch.NEWS_SOURCES = []
    mock_settings_patch.JINA_FETCH_DELAY_SECONDS = 0.1
    caplog.set_level(logging.INFO)

    # mock_fetch_article_content is not needed as it shouldn't be called
    with (
        patch(
            "app.data_ingestion.scheduler.fetch_article_content", new_callable=AsyncMock
        ) as mock_fetch_no_call,
        patch(
            "app.data_ingestion.scheduler.asyncio.sleep", new_callable=AsyncMock
        ) as mock_sleep_no_call,
    ):
        await perform_scheduled_article_fetch()

        mock_fetch_no_call.assert_not_called()
        mock_sleep_no_call.assert_not_called()

    caplog.set_level(logging.INFO)
    assert "Starting scheduled article fetch cycle..." in caplog.text
    assert (
        "Scheduled article fetch cycle completed. Fetched 0 out of 0 sources."
        in caplog.text
    )
    assert (
        "Fetching content from URL" not in caplog.text
    )  # Ensure no fetch attempts logged
