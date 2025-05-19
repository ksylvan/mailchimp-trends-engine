# Kubernetes Setup Guide for Mailchimp Trends Engine

This guide provides detailed instructions for setting up and managing the Kubernetes environment required for the Mailchimp Trends Engine project on macOS.

## Initial Setup

1. First, install Homebrew if you haven't already:

    ```bash
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    ```

2. Install Colima (provides Docker and Kubernetes support):

    ```bash
    brew install colima
    ```

3. Install Docker CLI tools:

    ```bash
    brew install docker docker-compose kubectl
    ```

4. Start Colima with Kubernetes enabled:

    ```bash
    colima start --kubernetes
    ```

5. Verify the installation:

    ```bash
    # Check Docker is working
    docker ps

    # Check Kubernetes is working
    kubectl get nodes
    ```

## Managing Kubernetes Context

After starting Colima with the `--kubernetes` flag, it automatically configures `kubectl` to use the new `colima` context. This means your `kubectl` commands will target the k3s cluster running within Colima.

You can manage and verify your Kubernetes contexts with the following commands:

```bash
# View available contexts
kubectl config get-contexts

# View current context
kubectl config current-context

# Switch context if needed
kubectl config use-context colima
```

## Common Operations

### Check System Status

```bash
# View all resources in your cluster
kubectl get all --all-namespaces

# Check Kubernetes system pods
kubectl get pods -n kube-system
```

### Resource Management

```bash
# View resource usage
colima list

# Monitor cluster resources
kubectl top nodes  # Requires metrics-server
kubectl top pods   # Requires metrics-server
```

## Deploying the Mailchimp Trends Engine

### 1. Apply Kubernetes Manifests

From the project root directory:

```bash
kubectl apply -f kubernetes/
```

### 2. Verify Deployment

```bash
# Check if pods are running
kubectl get pods

# Check services
kubectl get services

# View detailed information about a specific pod
kubectl describe pod <pod-name>
```

### 3. Access the Application

Once deployed, you can access:

- Backend API: <http://localhost:8000>
- Frontend Application: <http://localhost:3000>

## Troubleshooting

If you encounter issues:

### Reset Colima

```bash
colima delete
colima start --kubernetes # Or with your preferred CPU/memory settings
```

### Check Colima Status

```bash
colima status
```

### View Colima Logs

```bash
colima logs
```

### Common Fixes

- If Docker commands fail: Ensure Colima is running with `colima status` and start it if needed (`colima start`).
- If `kubectl` commands fail or don't see the `colima` context: Ensure Colima was started with `--kubernetes` (`colima stop && colima start --kubernetes`). Verify context with `kubectl config current-context`.
- If contexts are mixed up: Explicitly switch using `kubectl config use-context colima`.
- If pods are stuck in "Pending" state: Check resource requests/limits and node resources. Use `kubectl describe pod <pod-name>` for details.
- If pods have `ImagePullBackOff` or `ErrImagePull` status for locally built images:
  - Ensure your Kubernetes Deployment YAML specifies `imagePullPolicy: IfNotPresent` or `imagePullPolicy: Never`.
  - Verify the Docker image tag in your manifest matches the tag of the locally built image.
  - Ensure k3s can access the Docker daemon's images (Colima usually handles this by sharing the Docker socket).
- If services are not accessible from the host:
  - Verify the Service type (e.g., `NodePort`, `LoadBalancer`). For `NodePort`, find the port using `kubectl get svc <service-name>`.
  - Check if `kubectl port-forward service/<service-name> <local-port>:<service-port>` works for temporary access and diagnostics.

## Best Practices

### Resource Allocation

For this project, we recommend minimum:

```bash
colima start --kubernetes --cpu 4 --memory 8 --disk 100
```

### Persistence

- Colima persists your data in `~/.colima`
- Docker volumes are preserved between restarts
- For persistent storage in Kubernetes, use PersistentVolumeClaims

### Development Workflow

- Keep Colima running during development
- Use `colima stop` when not needed to free resources
- Regularly update with `brew upgrade colima`
- For development, use port forwarding: `kubectl port-forward service/<service-name> <local-port>:<service-port>`

## Updating Components

To update your setup:

```bash
brew update
brew upgrade colima docker kubectl
```

## Recommended Additional Tools

```bash
# k9s - Terminal UI for Kubernetes
brew install k9s

# kubectx - Easy context switching
brew install kubectx

# helm - Kubernetes package manager
brew install helm
```

## Project-Specific Configuration

The Mailchimp Trends Engine requires specific configurations for optimal performance:

### Environment Variables

Ensure your Kubernetes deployments include the necessary environment variables:

- `ANTHROPIC_API_KEY` - For Claude integration
- `JINA_API_KEY` - For Jina AI Reader (optional)

### Resource Limits

The recommended resource limits for our services:

- Backend: 2 CPU, 4GB RAM
- Frontend: 1 CPU, 2GB RAM
- NLP Processing: 2 CPU, 6GB RAM
