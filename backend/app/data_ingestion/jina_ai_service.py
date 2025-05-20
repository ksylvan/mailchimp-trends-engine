"""Jina AI Service for fetching article content.
This module provides a function to fetch the primary textual content of
a given URL using the Jina AI Reader API. It handles HTTP requests and
responses, including error handling for various scenarios.
"""

import logging
import urllib.parse

import httpx

logger = logging.getLogger(__name__)

USER_AGENT = "MailchimpTrendsEngine/1.0"
JINA_READER_BASE_URL = "https://r.jina.ai/"
DEFAULT_TIMEOUT = 30.0  # seconds


async def fetch_article_content(url: str, client: httpx.AsyncClient) -> str | None:
    """
    Fetches the primary textual content of a given URL using the Jina AI Reader API.

    Args:
        url: The URL of the article to fetch.
        client: An instance of httpx.AsyncClient.

    Returns:
        The extracted text content as a string if successful, otherwise None.
    """
    if not url:
        logger.warning("fetch_article_content called with empty URL.")
        return None

    encoded_url = urllib.parse.quote(url, safe="")
    jina_url = f"{JINA_READER_BASE_URL}{encoded_url}"
    headers = {
        "Accept": "text/plain",  # Request plain text for simplicity
        "User-Agent": USER_AGENT,
    }

    logger.info("Fetching content for URL: %s via Jina: %s", url, jina_url)

    try:
        response = await client.get(jina_url, headers=headers, timeout=DEFAULT_TIMEOUT)
        response.raise_for_status()  # Raises HTTPStatusError for 4xx/5xx responses
        logger.info("Successfully fetched content from Jina for URL: %s", url)
        return response.text
    except httpx.HTTPStatusError as e:
        logger.error(
            "HTTP error occurred when fetching %s "
            "via Jina: Status %s for %s. Response: %s",
            url,
            e.response.status_code,
            e.request.url,
            e.response.text[:500],
        )
        return None
    except httpx.RequestError as e:
        logger.error(
            "Request error occurred when fetching %s via Jina: %s for %s",
            url,
            e.__class__.__name__,
            e.request.url,
        )
        return None
    except Exception as e:
        logger.exception(
            "An unexpected error occurred when fetching %s via Jina: %s", url, e
        )
        return None
