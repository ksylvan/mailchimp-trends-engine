# Makefile for Mailchimp Trends Engine
#
# Ued to bootstrap the project, run the server, run tests, and other tasks.
#

.PHONY: help bootstrap test coverage coverage-html \
	install lint clean run docker docker-test docker-lint \
	docker-clean

help:
	@echo "Makefile for Mailchimp Trends Engine"
	@echo ""
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  bootstrap     Bootstrap the project"
	@echo "  clean         Clean up the project"
	@echo "  coverage      Run test coverage"
	@echo "  coverage-html Run tests and generate an HTML coverage report"
	@echo "  docker        Build and run the Docker container"
	@echo "  docker-clean  Clean up Docker containers and images"
	@echo "  docker-lint   Run linters in Docker container"
	@echo "  docker-test   Run tests in Docker container"
	@echo "  help          Show this help message"
	@echo "  install       Install dependencies"
	@echo "  lint          Run linters"
	@echo "  run           Run the server"
	@echo "  test          Run tests"

bootstrap:
	make -C backend bootstrap

install:
	@echo TODO: install Not yet implemented

test: lint
	make -C backend test

coverage:
	make -C backend coverage

lint:
	make -C backend lint

clean:
	make -C backend clean

run:
	@echo TODO: run Not yet implemented

docker:
	@echo TODO: docker Not yet implemented

docker-test:
	@echo TODO: docker-test Not yet implemented

docker-lint:
	@echo TODO: docker-lint Not yet implemented

docker-clean:
	@echo TODO: docker-clean Not yet implemented
