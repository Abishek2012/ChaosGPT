# ChaosGPT

ChaosGPT is an enterprise-grade, local-first AI-powered Chaos Engineering platform for Kubernetes, DevOps, MLOps, observability, AI agents, and GitOps.

This repository is organized as a production monorepo. Milestone 1 delivers a runnable control-plane foundation instead of a throwaway demo: typed domain models, a FastAPI API, a policy-first planner, Kubernetes discovery against a real cluster, local open-source dependencies, a Go orchestrator starter, CI, and documentation.

## Milestone Strategy

The platform is built in independently runnable milestones. This commit completes **Milestone 1: Control Plane Foundation**.

Milestone 1 includes:

- FastAPI control-plane service with health, planning, and live Kubernetes inventory endpoints.
- Clean domain/application/infrastructure separation for experiment plans and planner policy.
- Real Kubernetes discovery through the Kubernetes API; no mocked cluster inventory is returned.
- Local Docker Compose dependencies for PostgreSQL, Redis, NATS, Qdrant, Prometheus, and Grafana.
- Kind bootstrap script for a local Kubernetes cluster.
- Go orchestrator starter for experiment execution payloads.
- GitHub Actions for Python tests/lint, Go tests, and Docker image build.
- Architecture and deployment documentation.

## Repository Layout

```text
backend/                  FastAPI control plane, domain logic, infrastructure adapters, tests
cmd/chaos-orchestrator/   Go orchestration starter
frontend/                 React + TypeScript + Vite workspace placeholder for the console
infra/docker/             Local open-source services via Docker Compose
infra/terraform/          Terraform environment scaffold
deployments/kubernetes/   Kubernetes and Litmus manifests
docs/                     Architecture, deployment, and remediation docs
scripts/                  Local developer automation
.github/workflows/        CI pipeline
```

## Run Milestone 1 Locally

### 1. Install Python dependencies

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r backend/requirements-dev.txt
```

### 2. Start local platform dependencies

```bash
docker compose -f infra/docker/docker-compose.yml up -d
```

### 3. Start a local Kubernetes cluster

```bash
scripts/kind-up.sh
```

### 4. Run the API

```bash
PYTHONPATH=backend uvicorn app.main:app --reload
```

### 5. Create a production-guarded experiment plan

```bash
curl -X POST http://127.0.0.1:8000/api/v1/experiments/plans \
  -H "Content-Type: application/json" \
  -d '{"intent":"Simulate Black Friday","namespace":"production-canary","max_customer_impact_percent":5}'
```

### 6. Discover the local Kubernetes cluster

```bash
curl http://127.0.0.1:8000/api/v1/clusters/local/inventory
```

The inventory endpoint talks to the Kubernetes API directly and fails loudly if kubeconfig or the Kubernetes client is unavailable.

## Current Capabilities

- Cluster discovery: namespaces, deployments, pods, nodes, PVCs, services, and ingresses.
- Chaos planning for high-risk business scenarios with mandatory blast-radius controls.
- Failure-mode taxonomy covering CPU, memory, disk, pods, nodes, DNS, packet loss, latency, bandwidth, Redis, Kafka, PostgreSQL, APIs, PVCs, ConfigMaps, and Secrets.
- Local OSS dependencies: PostgreSQL, Redis, NATS, Qdrant, Prometheus, Grafana, Kind, Litmus, and Chaos Mesh-ready Kubernetes manifests.
- JWT helper functions for signed access tokens and role claims.

## Next Milestones

1. Persist experiments, approvals, schedules, audit logs, and reports in PostgreSQL with SQLAlchemy and Alembic.
2. Add LangGraph planner integration with Ollama and OpenAI-compatible APIs.
3. Implement Chaos Mesh and Litmus executors with approval gates and dry-run previews.
4. Add OpenTelemetry instrumentation and RCA ingestion from Prometheus, Loki, Tempo, and Kubernetes events.
5. Build the React/TypeScript/Tailwind operator console.
6. Add GitHub remediation PR generation for HPA, resources, retries, circuit breakers, and GitOps manifests.
