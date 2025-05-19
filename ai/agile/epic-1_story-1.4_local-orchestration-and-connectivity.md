# Story 1.4: Local Orchestration & Initial Frontend-Backend Connectivity (Colima/k3s)

## Status: Draft

## Story

- As a Developer Agent
- I want to set up local container orchestration using Colima/k3s and establish initial connectivity between the containerized frontend and backend applications
- so that the full application stack can be run and tested locally in a Kubernetes-like environment, ensuring services can communicate as expected.

## Acceptance Criteria (ACs)

1. Clear, concise documentation is created (e.g., in `docs/local-dev-setup.md` or `README.md` section) explaining how to set up Colima with k3s for this project.
2. Basic Kubernetes manifest files (e.g., Deployments, Services) are created in the `kubernetes/` directory for both the backend (FastAPI) and frontend (Next.js) applications.
3. Both backend and frontend applications can be successfully deployed to the local Colima/k3s cluster using these manifests (e.g., via `kubectl apply -f kubernetes/`).
4. The backend service is accessible within the k3s cluster and, if configured (e.g., via NodePort or LoadBalancer for local access), from the host machine.
5. The frontend service is accessible from the host machine's browser (e.g., via NodePort or LoadBalancer).
6. The frontend application successfully calls the backend's `/health` endpoint from within the k3s cluster (e.g., using the backend's k8s service name like `http://mailchimp-trends-backend-svc:8000/health`).
7. The frontend application displays the status (or an error message) received from the backend `/health` endpoint on its basic homepage.
8. The local orchestration setup is documented sufficiently for another developer to replicate it.

## Tasks / Subtasks

- [ ] Task 1: Document Colima/k3s Setup (AC: #1, #8)
  - [x] Create `docs/kubernetes-setup.md` (or a section in the main `README.md`).
  - [x] Provide step-by-step instructions for installing Colima.
  - [x] Provide instructions for starting Colima with k3s enabled (e.g., `colima start --kubernetes`).
  - [ ] Include steps for configuring `kubectl` to connect to the Colima k3s cluster.
  - [ ] Add troubleshooting tips for common issues.
- [ ] Task 2: Create Kubernetes Manifests for Backend (AC: #2)
  - [ ] Create `kubernetes/backend-deployment.yaml`:
    - [ ] Define a `Deployment` for the backend FastAPI application.
    - [ ] Use the Docker image built in Story 1.2 (e.g., `mailchimp-trends-backend:latest` or a locally tagged version).
    - [ ] Specify necessary environment variables (e.g., `PORT=8000`, `BACKEND_VERSION`). For secrets like API keys (post-MVP), use k8s Secrets.
    - [ ] Define resource requests/limits (optional for local, good practice).
    - [ ] Set up readiness and liveness probes targeting the `/health` endpoint.
  - [ ] Create `kubernetes/backend-service.yaml`:
    - [ ] Define a `Service` (e.g., ClusterIP type, named `mailchimp-trends-backend-svc`) to expose the backend deployment within the cluster on port 8000.
- [ ] Task 3: Create Kubernetes Manifests for Frontend (AC: #2)
  - [ ] Create `kubernetes/frontend-deployment.yaml`:
    - [ ] Define a `Deployment` for the frontend Next.js application.
    - [ ] Use the Docker image built in Story 1.3 (e.g., `mailchimp-trends-frontend:latest`).
    - [ ] Specify necessary environment variables (e.g., `PORT=3000`, `NEXT_PUBLIC_API_URL=http://mailchimp-trends-backend-svc:8000/api/v1`).
    - [ ] Define resource requests/limits (optional).
  - [ ] Create `kubernetes/frontend-service.yaml`:
    - [ ] Define a `Service` (e.g., NodePort or LoadBalancer type for local accessibility, named `mailchimp-trends-frontend-svc`) to expose the frontend deployment on port 3000.
- [ ] Task 4: Deploy Applications to Colima/k3s (AC: #3, #4, #5)
  - [ ] Ensure local Docker images for backend and frontend are available to k3s (e.g., by using Colima's Docker socket or pushing to a local k3s registry if set up, or setting `imagePullPolicy: Never/IfNotPresent` for locally built images).
  - [ ] Apply the manifests: `kubectl apply -f kubernetes/backend-deployment.yaml -f kubernetes/backend-service.yaml -f kubernetes/frontend-deployment.yaml -f kubernetes/frontend-service.yaml`.
  - [ ] Verify pods are running: `kubectl get pods`.
  - [ ] Verify services are created: `kubectl get svc`.
  - [ ] Access the frontend service from the host browser via its NodePort or LoadBalancer IP/port.
- [ ] Task 5: Implement Frontend to Backend `/health` Call (AC: #6, #7)
  - [ ] In the frontend application (e.g., `frontend/app/(dashboard)/page.tsx` or a dedicated component):
    - [ ] Add logic (e.g., in a `useEffect` hook) to call the backend's `/health` endpoint.
    - [ ] Ensure the `NEXT_PUBLIC_API_URL` in the frontend correctly points to the backend's k8s service name (e.g., `http://mailchimp-trends-backend-svc:8000/api/v1`). Note: The `/health` endpoint is typically at the root of the API service, not under `/api/v1` if `/api/v1` is a router prefix. Adjust URL accordingly (e.g. `http://mailchimp-trends-backend-svc:8000/health`).
    - [ ] Store the response (or error) in component state.
    - [ ] Display the status (e.g., "Backend Status: Healthy - Version 0.1.0") or an error message on the page.
- [ ] Task 6: Update Root Makefile (Optional)
  - [ ] Add targets to the root `Makefile` like `make deploy-k8s` (applies all manifests) and `make undeploy-k8s` (deletes all manifests).

## Dev Technical Guidance

- **Kubernetes Service Names:** When the frontend calls the backend from within the k3s cluster, it should use the backend's Kubernetes Service name (e.g., `mailchimp-trends-backend-svc`) as the hostname in the URL. Kubernetes DNS will resolve this.
- **`imagePullPolicy`:** For locally built Docker images that are not pushed to a remote registry, ensure your Kubernetes Deployments use `imagePullPolicy: IfNotPresent` or `imagePullPolicy: Never` to prevent k3s from trying to pull them from Docker Hub. If Colima shares Docker's image cache, this might not be an issue.
- **Frontend API URL Configuration:** The `NEXT_PUBLIC_API_URL` environment variable for the frontend deployment in k8s needs to be set to the *internal* k8s service URL of the backend (e.g., `http://mailchimp-trends-backend-svc:8000/api/v1`). The `apiClient.ts` in the frontend should use this variable.
- **Backend `/health` endpoint URL:** Double-check the exact path for the `/health` endpoint. If the FastAPI app has a root path or an `/api/v1` prefix for all routes, ensure the call from the frontend matches. Typically, `/health` is at the root (e.g., `http://mailchimp-trends-backend-svc:8000/health`).
- **Exposing Frontend Service:** For local access from your browser to the frontend running in k3s, use a `Service` of type `NodePort` or `LoadBalancer`. `LoadBalancer` might require additional setup with Colima (e.g., MetalLB or similar if not built-in). `NodePort` is usually simpler for basic local access.
- **Readiness/Liveness Probes:** Implementing these for the backend Deployment targeting `/health` is good practice for k8s to manage pod health.

## Story Progress Notes

### Completion Notes List

{Any notes about implementation choices, difficulties, or follow-up needed}

### Change Log

- 2025-05-17 - Kayvan Sylvan - Initial draft
