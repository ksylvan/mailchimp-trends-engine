# Makefile for frontend
#

.PHONY: help bootstrap test coverage coverage-html lint clean \
	run dev build start help docker-build docker-run docker-stop format

VERSION := $(shell node -e "console.log(require('./package.json').version)")

help:
	@echo "Makefile for frontend"
	@echo ""
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  bootstrap     Bootstrap the project (install dependencies)"
	@echo "  build         Build the Next.js project for production"
	@echo "  clean         Clean up the project"
	@echo "  dev           Run the development server"
	@echo "  docker-build  Build the Docker image for the frontend"
	@echo "  docker-run    Run the frontend application using Docker"
	@echo "  docker-stop   Stop running Docker container"
	@echo "  format        Format the codebase with Prettier"
	@echo "  help          Show this help message"
	@echo "  lint          Run ESLint"
	@echo "  start         Start the production server"
	@echo "  tag           Tag the current git HEAD with the semantic versioning name"
	@echo "  test          Run tests"

bootstrap:
	pnpm install
	@echo "Frontend dependencies installed"

test: lint
	pnpm test

coverage:
	pnpm test:cov

coverage-html:
	@echo "To generate HTML coverage report, ensure your Jest config outputs 'html' reporter."
	@echo "Typically, you can run 'pnpm test:cov' and check the coverage/lcov-report/index.html file."
	pnpm test:cov # This will generate reports based on jest.config.js (text, lcov, etc.)

lint:
	pnpm lint

format:
	pnpm format

# Target to build the application for production
build:
	pnpm build

# Target to run the development server
dev:
	pnpm dev

# Target to start the production server
start:
	pnpm start

# Target to build the Docker image
docker-build:
	docker build -t mailchimp-trends-frontend:$(VERSION) -t mailchimp-trends-frontend:latest .

# Target to run the frontend application using Docker
docker-run: docker-build
	@echo "Stopping existing frontend container if any..."
	-docker stop mailchimp-trends-frontend-container
	@echo "Running frontend container. Access at http://localhost:3000"
	docker run -d -p 3000:3000 --rm --name mailchimp-trends-frontend-container mailchimp-trends-frontend:latest

# Target to stop the running Docker container
docker-stop:
	@echo "Stopping frontend container..."
	-docker stop mailchimp-trends-frontend-container

clean:
	rm -rf node_modules .next out
	@echo "Cleaned node_modules, .next, and out directories"

tag:
	git tag v$(VERSION)
