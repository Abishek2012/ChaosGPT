# ADR 001: integrated platform decisions

- **Kubernetes:** portable scheduling, rollout and isolation controls justify its operational cost for managed inference.
- **Argo CD/GitOps:** audited desired state and drift correction are safer than direct CI cluster access.
- **MLflow:** open experiment/model registry interface separates lifecycle provenance from serving.
- **HPA + optional KEDA:** resource and demand signals handle both sustained and event-driven load.
- **OpenCost:** exposes allocation and idle-cost signals without pretending application telemetry is billing.
- **Chaos Mesh:** declarative, selector-scoped experiments support measurable reliability hypotheses.
- **OpenTelemetry:** vendor-neutral traces/log correlation avoids coupling the service to one backend.
