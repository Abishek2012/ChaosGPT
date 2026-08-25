# Production readiness checklist

| Area | Implemented | Required before enterprise production |
|---|---|---|
| Security | non-root, policies, scan/SBOM/signing workflow | enforce policies/signature verification, external secret manager |
| Reliability | probes, PDB, HPA, 99.9% SLO metric contract | multi-AZ, load tests, runbooks and on-call |
| Observability | metrics, alerts, dashboard definition | managed retention, paging routes, trace/log collectors |
| Deployment | immutable GitOps desired state and rollback procedure | protected environments and approval/audit controls |
| DR | portable stateful dependency design | backup/restore drills and RTO/RPO ownership |
| Cost | OpenCost integration design, transparent local estimate | validated cloud rates, tags/allocation rules and budget alerts |
