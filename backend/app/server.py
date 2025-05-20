"""FastAPI server with logging and health check endpoint."""

import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .__about__ import __version__
from .api.v1.routers import data_ingestion as data_ingestion_router
from .data_ingestion.scheduler import shutdown_scheduler, start_scheduler

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(current_app: FastAPI):
    """Ensure proper startup and shutdown of the application."""
    logger.info("Application startup. Version: %s", current_app.version)
    logger.info("API documentation available at /docs or /redoc")
    await start_scheduler()
    yield
    # Shutdown
    await shutdown_scheduler()
    logger.info("Application shutdown.")


app = FastAPI(version=__version__, lifespan=lifespan)

# CORS Middleware Configuration
# Allow requests from the frontend development server and deployed frontend (NodePort)
# The NodePort for frontend is 30900, so localhost:30900
# Allow frontend development server (e.g., localhost:3000)
origins = [
    # TODO: Make this configurable via a config file in the future.
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

# Include API routers
app.include_router(
    data_ingestion_router.router,
    prefix="/api/v1/data-ingestion",
    tags=["Data Ingestion"],
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
