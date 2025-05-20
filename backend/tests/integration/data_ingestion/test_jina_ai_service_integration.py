"""Integration test for the Jina AI Reader API service."""

import httpx
import pytest

# Corrected import path
from backend.app.data_ingestion.jina_ai_service import fetch_article_content


@pytest.mark.integration
@pytest.mark.asyncio
async def test_fetch_example_dot_com_content():
    """
    Integration test for fetch_article_content.
    Fetches content from http://example.com using the Jina AI Reader API.
    This test makes a real network request.
    """
    target_url = "http://example.com"

    # Using a timeout to prevent tests from hanging indefinitely
    # httpx.AsyncClient should be used within an async context manager
    async with httpx.AsyncClient(timeout=30.0) as client:
        content = await fetch_article_content(target_url, client)

    assert content is not None, (
        f"Failed to fetch content from {target_url} via Jina. Content was None."
    )
    assert isinstance(content, str), "Fetched content is not a string."

    # Check for expected substrings from example.com
    # Jina might add its own formatting or extract specific parts,
    # so assertions should be somewhat flexible.
    # Common phrases on example.com:
    assert "Example Domain" in content, "Content should contain 'Example Domain'"
    assert "illustrative examples" in content, (
        "Content should contain 'illustrative examples'"
    )
    assert "documents" in content, "Content should contain 'documents'"

    # Log the fetched content for manual inspection if needed during test runs
    log_message = (
        f"Fetched content from {target_url} via Jina "
        f"(first 500 chars):\n{content[:500]}"
    )
    print(log_message)
