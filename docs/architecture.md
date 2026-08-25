# Architecture and portability

The workload is one FastAPI deployment rather than gratuitous microservices. MLflow tracks and promotes model artifacts; MinIO/S3-compatible object storage stores artifacts; PostgreSQL is the production MLflow backend. Argo CD continuously reconciles Helm desired state. Prometheus, Grafana, OpenTelemetry and Loki cover metrics, traces and logs. OpenCost converts cluster allocations into estimates.

| Capability | Local | AWS | Azure | GCP |
|---|---|---|---|---|
| Kubernetes | kind | EKS | AKS | GKE |
| Registry | local/GHCR | ECR | ACR | Artifact Registry |
| artifacts | MinIO | S3 | Blob Storage | GCS |
| MLflow DB | PostgreSQL | RDS | Azure Database | Cloud SQL |

Infrastructure interfaces are Kubernetes/OCI/S3 compatible, avoiding provider-specific application code. Terraform modules are intentionally provider-neutral contracts that cloud implementations can satisfy.
