# Makefile for Mailchimp Trends Engine
#
# Ued to bootstrap the project, run the server, run tests, and other tasks.
#

.PHONY: help bootstrap test coverage coverage-html \
	install lint clean run docker docker-test docker-lint \
	docker-clean build

help:
	@echo "Makefile for Mailchimp Trends Engine"
	@echo ""
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  bootstrap     Bootstrap the project"
	@echo "  build         Build the project"
	@echo "  clean         Clean up the project"
	@echo "  coverage      Run test coverage"
	@echo "  coverage-html Run tests and generate an HTML coverage report"
	@echo "  docker-build  Build the Docker image for the backend"
	@echo "  docker-run    Run the backend application using Docker"
	@echo "  format        Format the codebase"
	@echo "  help          Show this help message"
	@echo "  lint          Run linters"
	@echo "  run           Run the server"
	@echo "  tag           Tag the current git HEAD with the semantic versioning name."
	@echo "  test          Run tests"

bootstrap build clean coverage coverage-html format docker-build docker-run lint tag test:
	make -C backend $@

