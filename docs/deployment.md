# Deployment and GitOps

CI validates a model, scans/signs a SHA-tagged OCI image, and changes `gitops/environments/<env>/values.yaml`. It has no `kubectl` deployment step. Argo detects, diffs, self-heals, reports health, and supplies `argocd app rollback` for declarative rollback. That separation gives an auditable desired state and removes cluster credentials from CI.

Use `make setup-cluster`, install Argo/Prometheus/OpenCost by their official charts, then apply `gitops/applications/inference-dev.yaml` after replacing its repository URL. The local `make deploy` command is explicitly a development substitute, not the production delivery path. Promote only after `development → staging → production` validation and change approval; rollback by pinning the previous immutable tag in the environment values.

HPA uses CPU and memory; install Prometheus Adapter to add the request-rate external metric. KEDA may scale queued/burst workloads when an HTTP/queue trigger is available. Request-based signals avoid under-scaling I/O-bound inference.
