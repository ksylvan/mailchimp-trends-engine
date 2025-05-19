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
	@echo "  format        Format the codebase"
	@echo "  help          Show this help message"
	@echo "  lint          Run linters"
	@echo "  run           Run the project"
	@echo "  tag           Tag the current git HEAD with the semantic versioning name."
	@echo "  test          Run tests"

bootstrap:
	uv sync --dev
	@echo "Symlinking backend/.venv to top-level directory"
	ln -sf $(shell pwd)/.venv ..

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

build:
	@echo "TODO: build not implemented"

run:
	@echo "TODO: run not implemented"

clean:
	rm -f ../.venv && rm -rf .venv

tag:
	git tag v$(VERSION)
