"""Configuration settings for the application.
This module uses Pydantic to manage application settings, including
environment variables, default values, and validation.
It also sets up basic logging configuration."""

import logging

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings.
    """

    APP_NAME: str = "Mailchimp Trends Engine"
    APP_VERSION: str = "0.1.0"  # Default version
    LOG_LEVEL: str = "INFO"

    # News sources for Jina AI Reader
    NEWS_SOURCES: list[str] = [
        "https://www.wired.com/most-recent/",
        "https://www.technologyreview.com/latest/",
        "https://www.marketingdive.com/",
    ]

    # Delay between Jina AI Reader fetches to respect rate limits
    JINA_FETCH_DELAY_SECONDS: float = 4.0

    SCHEDULER_PROCESSING_DELAY_SECONDS: float = 0.1

    CORS_ORIGINS: list[str] = [
        "http://localhost",  # General localhost for flexibility if needed
        "http://localhost:3000",  # Common local dev port for frontend
        "http://localhost:30900",  # Current Frontend NodePort
        "https://your-production-domain.com",
    ]

    # Example of another setting that might be needed later
    # ANTHROPIC_API_KEY: Optional[str] = None

    model_config = SettingsConfigDict(
        env_file=".env", extra="ignore", case_sensitive=False
    )


settings = Settings()

# Basic logging configuration
# This can be expanded or moved to a dedicated logging setup function if needed
logging.basicConfig(level=settings.LOG_LEVEL.upper())
logger = logging.getLogger(__name__)

logger.info("Settings loaded for %s v%s", settings.APP_NAME, settings.APP_VERSION)
logger.debug("Full settings: %s", settings.model_dump_json(indent=2))
