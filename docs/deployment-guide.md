# Local Deployment Guide

1. Start dependencies with `docker compose -f infra/docker/docker-compose.yml up -d`.
2. Create a local Kubernetes cluster with `scripts/kind-up.sh`.
3. Install Chaos Mesh and Litmus from their upstream Helm charts.
4. Build and run the API with `docker build -f backend/Dockerfile -t chaosgpt-api .` and `docker run --network host chaosgpt-api`.
5. Apply Kubernetes manifests with `kubectl apply -f deployments/kubernetes/`.
