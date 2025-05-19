"""FastAPI server with logging and health check endpoint."""

import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .__about__ import __version__

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(current_app: FastAPI):
    """Ensure proper startup and shutdown of the application."""
    logger.info("Application startup. Version: %s", current_app.version)
    logger.info("API documentation available at /docs or /redoc")
    yield
    # Shutdown
    logger.info("Application shutdown.")


app = FastAPI(version=__version__, lifespan=lifespan)

# CORS Middleware Configuration
# Allow requests from the frontend development server and deployed frontend (NodePort)
# The NodePort for frontend is 30306, so localhost:30306
# Allow frontend development server (e.g., localhost:3000)
origins = [
    "http://localhost",  # General localhost for flexibility if needed
    "http://localhost:3000",  # Common local dev port for frontend
    "http://localhost:30900",  # Current Frontend NodePort
    # Add any other origins if necessary, e.g., deployed frontend URL post-MVP
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


@app.get("/health")
async def health_check():
    """
    Health check endpoint.
    """
    return {"status": "healthy", "version": app.version}


def main(log_level: str = "info") -> None:
    """
    Main function to run the FastAPI application.
    """
    logger.info("Starting server with version: %s", __version__)
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level=log_level)
