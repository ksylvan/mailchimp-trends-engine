# Mailchimp Marketing Trends Engine - Backend

This is the backend for the Mailchimp Marketing Trends Engine, a powerful FastAPI application built with Python. It's the core engine that processes web content, identifies emerging marketing trends, and generates AI-powered content suggestions.

## Key Technologies

* **FastAPI:** For building high-performance APIs with Python.
* **Python:** The primary programming language.
* **Hugging Face Transformers:** For advanced NLP tasks like topic extraction and sentiment analysis.
* **Jina AI Reader:** Integrated for efficient web content extraction.
* **Anthropic Claude:** Powers the AI content generation features.
* **uv:** For modern Python environment and package management.

## Core Functionality

* Ingests and processes articles from configured news sources.
* Applies NLP techniques to extract topics and analyze sentiment.
* Assesses the marketing relevance of identified topics.
* Implements a trend identification algorithm based on frequency and growth.
* Provides API endpoints for the frontend to consume trend data and AI-generated content.
* Integrates with Anthropic Claude for generating marketing copy, email subject lines, and campaign themes.

## Getting Started

### Prerequisites

* Python (version as defined in project, e.g., 3.10+)
* [uv](https://github.com/astral-sh/uv) (Python package installer)
* Access to a running instance of any required external services (e.g., database, message queue if applicable later).
* API Keys:
  * Anthropic API key (for Claude integration)
  * Jina AI API key (if used directly by backend services beyond what's orchestrated)

### Environment Setup

1. **Navigate to the backend directory:**

   ```bash
   cd backend
   ```

2. **Create and activate a virtual environment (using uv):**

   ```bash
   uv sync
   source .venv/bin/activate
   ```

3. **Configure environment variables:**
   * Copy the example environment file:

     ```bash
     cp .env.example .env
     ```

   * Edit the `.env` file with your specific configurations, including API keys and database connection strings.

### Running the Application

* **Development server:**

  ```bash
  uvicorn app.main:app --reload
  ```

  (Assuming your FastAPI application instance is in `app/main.py` and named `app`)

  The API will typically be available at `http://localhost:8000`.

## Project Structure (Illustrative)

```text
backend/
├── app/                    # Main application code
│   ├── __init__.py
│   ├── main.py             # FastAPI app definition and root endpoints
│   ├── api/                # API endpoint routers
│   │   └── v1/
│   │       ├── __init__.py
│   │       └── trends.py   # Example: Trend related endpoints
│   ├── core/               # Core logic, configuration, settings
│   │   └── config.py
│   ├── services/           # Business logic services (e.g., nlp, data_ingestion)
│   │   └── nlp_service.py
│   ├── models/             # Pydantic models, SQLAlchemy models (if used)
│   │   └── trend_models.py
│   └── schemas/            # Pydantic schemas for API request/response validation
│       └── trend_schemas.py
├── tests/                  # Unit and integration tests
├── .env                    # Local environment variables (DO NOT COMMIT)
├── .env.example            # Example environment variables
├── pyproject.toml          # Project metadata and dependencies (using uv/Poetry/PDM)
├── README.md               # This file
└── ...                     # Other configuration files (linters, formatters)
```

This README provides a starting point. Ensure to update it as the backend evolves, especially regarding specific setup instructions, new dependencies, or changes in the run commands.
