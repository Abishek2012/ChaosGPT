# ChaosGPT Milestones

ChaosGPT is delivered as independently runnable milestones. A milestone is complete only when it includes code, tests, documentation, and local execution commands.

## Milestone 1: Control Plane Foundation

Status: complete.

Scope:

- Typed experiment domain model and blast-radius policy validation.
- FastAPI endpoints for health, plan creation, and Kubernetes inventory.
- Real Kubernetes discovery through kubeconfig and the Kubernetes API.
- Local open-source dependencies through Docker Compose.
- Kind bootstrap script, CI workflow, Dockerfile, and deployment documentation.

Validation commands:

```bash
PYTHONPATH=backend python3 -m pytest backend/tests
python3 -m compileall -q backend/app
go test ./...
git diff --check
```

## Milestone 2: Persistence, Audit, and Approvals

Planned scope:

- SQLAlchemy repositories for experiments, approvals, schedules, audit events, and reports.
- Alembic migrations for PostgreSQL.
- Redis-backed rate limiting and short-lived workflow locks.
- JWT authentication middleware and RBAC enforcement on mutating endpoints.
- Integration tests against local PostgreSQL and Redis.

## Milestone 3: AI Planner and RCA Agent

Planned scope:

- LangGraph workflow for planning, safety review, execution summary, and RCA generation.
- Ollama and OpenAI-compatible model adapters.
- Qdrant-backed embeddings for runbooks, prior incidents, and remediation patterns.
- Prompt-injection controls and policy validation before execution.

## Milestone 4: Chaos Execution

Planned scope:

- Chaos Mesh and Litmus executors.
- Dry-run previews, approval workflow, and scheduler support.
- Experiment event streaming over NATS.
- Rollback hooks for failed or unsafe experiments.

## Milestone 5: Observability and Reports

Planned scope:

- OpenTelemetry instrumentation.
- Prometheus, Loki, Tempo, and Kubernetes event ingestion.
- Markdown, JSON, and PDF reports.
- Timeline, blast-radius, root-cause, and recommendation generation.

## Milestone 6: Operator Console and GitOps Remediation

Planned scope:

- React, TypeScript, Vite, and Tailwind operator console.
- GitHub pull request generation for HPA, resource, retry, circuit-breaker, and GitOps manifest changes.
- ArgoCD application manifests and Terraform modules for repeatable local deployment.
