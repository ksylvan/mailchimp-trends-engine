# Mailchimp Marketing Trends Engine (MVP)

A real-time marketing trends analysis engine that scans web content to identify emerging marketing trends and generates AI-powered content suggestions for Mailchimp users. This system helps marketers stay ahead of trends and create timely, relevant marketing campaigns.

## Overview

The Mailchimp Marketing Trends Engine processes web content in real-time to:

- Identify and analyze emerging marketing trends using NLP and topic modeling
- Assess marketing relevance and trend significance
- Generate AI-powered content suggestions for email campaigns
- Visualize trend evolution and significance through an intuitive dashboard

### Key Features (MVP)

- **Real-time Trend Analysis**
  - Web content extraction using Jina AI Reader
  - NLP-based topic extraction and sentiment analysis
  - Marketing relevance assessment with configurable ontology
  - Trend scoring based on frequency and growth rate

- **Interactive Dashboard**
  - Trend visualization with category/sentiment filtering
  - Time-series analysis of trend evolution
  - Mailchimp-aligned UI/UX design

- **AI Content Generation**
  - Marketing copy suggestions using Anthropic Claude
  - Email subject lines and campaign themes
  - One-click copy-to-clipboard functionality

## Technical Architecture

### Stack Overview

- **Backend**
  - Python/FastAPI application
  - NLP processing pipeline using Hugging Face Transformers
  - Jina AI Reader integration for content extraction
  - Anthropic Claude integration for content generation
  - uv for Python environment and package management

- **Frontend**
  - TypeScript/Next.js
  - Tailwind CSS with shadcn/ui components
  - Real-time data visualization
  - pnpm for package management

- **Infrastructure**
  - Docker containers
  - Local orchestration with Colima/k3s
  - GitHub Actions CI/CD pipeline

## Getting Started

### Prerequisites

- Docker Desktop (or compatible Docker engine)
- Colima with k3s support ([see detailed Kubernetes setup guide](docs/kubernetes-setup.md))
- [uv](https://github.com/astral-sh/uv) - Modern Python package installer and resolver
- pnpm - Fast Node.js package manager
- Required API keys:
  - Anthropic API key (for Claude integration)
  - Jina AI API key (optional, for enhanced search capability)

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-org/mailchimp-trends-engine.git
   cd mailchimp-trends-engine
   ```

2. Configure environment:

   ```bash
   # Copy example environment files
   cp backend/.env.example backend/.env
   cp frontend/.env.example frontend/.env

   # Edit .env files with your API keys and configuration
   ```

3. Start local environment:

   ```bash
   # Ensure Colima is running with k3s
   colima start --kubernetes

   # Apply Kubernetes manifests
   kubectl apply -f kubernetes/
   ```

### Local Development

The project supports both containerized and local development workflows:

For detailed instructions on setting up and managing the Kubernetes environment, including troubleshooting and best practices, please refer to our [Kubernetes Setup Guide](docs/kubernetes-setup.md).

#### Containerized Development

```bash
# Build and run all services
kubectl apply -f kubernetes/

# View service status
kubectl get pods
```

#### Local Native Development

```bash
# Backend
cd backend
uv sync  # Sets up virtual environment and installs/updates all requirements

# uv run automatically activates the venv and runs the command in one step
uv run uvicorn mailchimp_trends.main:app --reload

# Frontend
cd frontend
pnpm install
pnpm dev
```

## Project Structure

```plaintext
mailchimp-trends-engine/
├── backend/                 # FastAPI application
│   ├── src/
│   │   └── mailchimp_trends/
│   │       ├── main.py     # FastAPI app entry point
│   │       ├── api/        # API routers/endpoints
│   │       ├── core/       # Core logic, config
│   │       ├── data_ingestion/
│   │       ├── nlp_processing/
│   │       ├── trend_identification/
│   │       ├── llm_integration/
│   │       └── models/     # Pydantic models
│   └── tests/
├── frontend/               # Next.js application
│   ├── app/               # Next.js app directory
│   ├── components/
│   ├── public/
│   └── styles/
├── kubernetes/            # K8s manifests
├── docs/                  # Documentation
└── .github/              # GitHub Actions
```

## Development Workflow

### Testing

```bash
# Backend tests
cd backend
# Install test dependencies and update environment
uv sync --extras test

# Run tests with automatic venv activation
uv run pytest

# Frontend tests
cd frontend
pnpm test
```

### CI/CD Pipeline

The project uses GitHub Actions for continuous integration:

- Automated testing with pytest and Jest
- Linting with Ruff
- Type checking with mypy
- Docker image builds
- Kubernetes manifest validation

## Environment Variables

### Backend (.env)

```bash
ANTHROPIC_API_KEY=your_api_key_here
JINA_API_KEY=your_api_key_here  # Optional
```

### Frontend (.env)

```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## API Documentation

When running locally, API documentation is available at:

- Swagger UI: <http://localhost:8000/docs>
- ReDoc: <http://localhost:8000/redoc>

## Project Documentation

For detailed information about the project, refer to:

- [Product Requirements Document](docs/prd.md)
- [Project Brief](docs/project-brief.md)
- [Technical Documentation](docs/)

## License

[Include appropriate license information]
