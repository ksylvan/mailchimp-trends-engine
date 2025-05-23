# Makefile for Mailchimp Trends Engine
#
# Used to bootstrap the project, run the server, run tests, and other tasks.
#

.PHONY: help bootstrap test coverage coverage-html \
	install lint clean run dev docker-build docker-run docker-stop \
	docker-clean build frontend backend format \
	deploy-k8s undeploy-k8s

help:
	@echo "Makefile for Mailchimp Trends Engine"
	@echo ""
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  bootstrap     Bootstrap the project (both frontend and backend)"
	@echo "  build         Build the project (both frontend and backend)"
	@echo "  clean         Clean up the project (both frontend and backend)"
	@echo "  coverage      Run test coverage (both frontend and backend)"
	@echo "  coverage-html Run tests and generate an HTML coverage report (both frontend and backend)"
	@echo "  dev           Run the frontend development server"
	@echo "  docker-build  Build Docker images for both frontend and backend"
	@echo "  docker-run    Run both frontend and backend using Docker"
	@echo "  docker-stop   Stop running Docker containers"
	@echo "  format        Format the codebase (both frontend and backend)"
	@echo "  help          Show this help message"
	@echo "  lint          Run linters (both frontend and backend)"
	@echo "  run           Run the backend server"
	@echo "  start         Start the production frontend server"
	@echo "  tag           Tag the current git HEAD with the semantic versioning name"
	@echo "  test          Run tests (both frontend and backend)"
	@echo "  deploy-k8s    Deploy applications to local k3s cluster"
	@echo "  undeploy-k8s  Remove applications from local k3s cluster"
	@echo ""
	@echo "Prefixed targets:"
	@echo "  backend-*     Run target only for backend (e.g., make backend-test)"
	@echo "  frontend-*    Run target only for frontend (e.g., make frontend-dev)"

# Default handling of common commands: run for both backend and frontend
bootstrap build clean coverage coverage-html docker-build docker-run docker-stop format lint tag test:
	@echo "Running $@ for backend..."
	@make -C backend $@
	@echo "Running $@ for frontend..."
	@make -C frontend $@

# Backend specific commands
backend:
	@echo "Please specify a target for backend (e.g., backend-test)"
	@exit 1

backend-%:
	@target=$$(echo $@ | sed 's/^backend-//'); \
	echo "Running $$target for backend..."; \
	make -C backend $$target

# Frontend specific commands
frontend frontend-%:
	@target=$$(echo $@ | sed 's/^frontend-//'); \
	if [ "$$target" = "frontend" ]; then \
		echo "Please specify a target for frontend (e.g., frontend-dev)"; \
		exit 1; \
	fi; \
	echo "Running $$target for frontend..."; \
	make -C frontend $$target

# Special handling for specific commands
run:
	@echo "Running backend server..."
	@make -C backend run

dev:
	@echo "Running frontend development server..."
	@make -C frontend dev

start:
	@echo "Starting frontend production server..."
	@make -C frontend start

# Kubernetes deployment commands
deploy-k8s:
	@echo "Deploying applications to local k3s cluster..."
	kubectl apply -f kubernetes/backend-deployment.yaml
	kubectl apply -f kubernetes/backend-service.yaml
	kubectl apply -f kubernetes/frontend-deployment.yaml
	kubectl apply -f kubernetes/frontend-service.yaml
	@echo "Verifying deployments..."
	kubectl wait --for=condition=ready pod -l app=mailchimp-trends-backend --timeout=60s
	kubectl wait --for=condition=ready pod -l app=mailchimp-trends-frontend --timeout=60s
	kubectl get pods -l app=mailchimp-trends-backend
	kubectl get pods -l app=mailchimp-trends-frontend
	kubectl get svc mailchimp-trends-backend-svc
	kubectl get svc mailchimp-trends-frontend-svc

undeploy-k8s:
	@echo "Removing applications from local k3s cluster..."
	kubectl delete -f kubernetes/frontend-service.yaml --ignore-not-found=true
	kubectl delete -f kubernetes/frontend-deployment.yaml --ignore-not-found=true
	kubectl delete -f kubernetes/backend-service.yaml --ignore-not-found=true
	kubectl delete -f kubernetes/backend-deployment.yaml --ignore-not-found=true
	@echo "Verifying removal..."
	kubectl get pods
	kubectl get svc
