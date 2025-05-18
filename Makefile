# Makefile for Mailchimp Trends Engine
#
# Ued to bootstrap the project, run the server, run tests, and other tasks.
#

.PHONY: help install test coverage lint clean \
	run help bootstrap docker docker-test docker-lint docker-clean

help:
	@echo "Makefile for Mailchimp Trends Engine"
	@echo ""
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  install   - Install dependencies"
	@echo "  test      - Run tests"
	@echo "  coverage  - Run test coverage"
	@echo "  lint      - Run linters"
	@echo "  clean     - Clean up the project"
	@echo "  run       - Run the server"
	@echo "  help      - Show this help message"
	@echo "  bootstrap  - Bootstrap the project"
	@echo "  docker     - Build and run the Docker container"
	@echo "  docker-test - Run tests in Docker container"
	@echo "  docker-lint - Run linters in Docker container"
	@echo "  docker-clean - Clean up Docker containers and images"

install:
	@echo TODO: install Not yet implemented

test: lint
	@echo TODO: test Not yet implemented

coverage:
	@echo TODO: coverage Not yet implemented

lint:
	@echo TODO: lint Not yet implemented

clean:
	@echo TODO: clean Not yet implemented

run:
	@echo TODO: run Not yet implemented

bootstrap:
	@echo TODO: bootstrap Not yet implemented

docker:
	@echo TODO: docker Not yet implemented

docker-test:
	@echo TODO: docker-test Not yet implemented

docker-lint:
	@echo TODO: docker-lint Not yet implemented

docker-clean:
	@echo TODO: docker-clean Not yet implemented