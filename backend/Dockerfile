# Use an official Python runtime as a parent image
FROM python:3.13-slim AS base

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV UV_EXTRA_INDEX_URL=""

# Install uv
RUN pip install uv

# Create a non-root user
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser
WORKDIR /home/appuser

# --- Builder stage ---
FROM base AS builder
WORKDIR /home/appuser

# Copy project files for dependency installation
COPY pyproject.toml uv.lock ./
COPY README.md ./
# Copy the app directory as well, because hatch needs app/__about__.py to determine version during install
COPY app/ ./app

# Install dependencies using uv from the lock file
# Using --frozen to ensure it uses uv.lock and doesn't update it
# Not installing --dev dependencies for production image
RUN uv sync --no-cache --frozen

# --- Final stage ---
FROM base AS final
WORKDIR /home/appuser

# Copy installed dependencies from builder stage
COPY --from=builder /home/appuser/.venv ./.venv
ENV PATH="/home/appuser/.venv/bin:$PATH"

# Copy the application code
# The pyproject.toml specifies 'packages = ["app"]'
# and dev-mode-dirs = ["app"]
# This means our application code is in the 'app' directory.
COPY app/ ./app

# Switch to non-root user
USER appuser

# Expose port 8000 (standard for FastAPI with Uvicorn)
EXPOSE 8000

# Command to run the application
# The app object is in app.server:app
CMD ["uvicorn", "app.server:app", "--host", "0.0.0.0", "--port", "8000"]
