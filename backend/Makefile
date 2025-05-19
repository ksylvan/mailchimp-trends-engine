# Makefile for backend
#

.PHONY: help bootstrap test coverage coverage-html lint clean \
	run help build

COVERAGE_FAIL_UNDER := 90
COVERAGE_SRC := app

VERSION := $(shell uv run hatch version)

help:
	@echo "Makefile for backend"
	@echo ""
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  bootstrap     Bootstrap the project"
	@echo "  build         Build the project"
	@echo "  clean         Clean up the project"
	@echo "  coverage      Run test coverage"
	@echo "  coverage-html Run tests and generate an HTML coverage report."
	@echo "  docker-build  Build the Docker image for the backend"
	@echo "  docker-run    Run the backend application using Docker"
	@echo "  format        Format the codebase"
	@echo "  help          Show this help message"
	@echo "  lint          Run linters"
	@echo "  run           Run the dev server locally using uvicorn"
	@echo "  tag           Tag the current git HEAD with the semantic versioning name."
	@echo "  test          Run tests"

bootstrap:
	uv sync --dev
	@echo "Symlinking backend/.venv to top-level directory"
	# Create a symlink from backend/.venv to ../.venv if it doesn't exist or is not already a symlink to the correct target
	if [ ! -L ../.venv ] || [ "$$(readlink ../.venv)" != "$$(pwd)/.venv" ]; then \
		ln -sf $(shell pwd)/.venv .. ;\
	fi

test: lint
	uv run pytest -v

coverage:
	uv run pytest --cov=$(COVERAGE_SRC) \
		-ra -q \
		--cov-report=term-missing \
		--cov-fail-under=$(COVERAGE_FAIL_UNDER)

coverage-html:
	# This will generate an HTML coverage report.
	uv run pytest --cov=$(COVERAGE_SRC) \
		--cov-report=html:coverage_html \
		--cov-fail-under=$(COVERAGE_FAIL_UNDER)


lint:
	uv run ruff check .
	uv run pylint .

format:
	uv run ruff format .
	uv run isort .

# Target to build the application's source distribution and wheel
build:
	uv run hatch build

# Target to build the Docker image
docker-build:
	docker build -t mailchimp-trends-backend:$(VERSION) -t mailchimp-trends-backend:latest .

# Target to run the application using uvicorn for local development
run:
	uv run uvicorn app.server:app --reload --host 0.0.0.0 --port 8000

# Target to run the backend application using Docker
docker-run: docker-build
	@echo "Stopping existing backend container if any..."
	-docker stop mailchimp-trends-backend-container
	@echo "Running backend container. Access at http://localhost:8000/health"
	docker run -d -p 8000:8000 --rm --name mailchimp-trends-backend-container mailchimp-trends-backend:latest

# Target to stop the running Docker container
docker-stop:
	@echo "Stopping backend container..."
	-docker stop mailchimp-trends-backend-container

clean:
	rm -f ../.venv && rm -rf .venv && rm -rf dist

tag:
	git tag v$(VERSION)
