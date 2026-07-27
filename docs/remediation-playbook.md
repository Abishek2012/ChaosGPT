# ChaosGPT Remediation Playbook

When an experiment breaches an SLO, ChaosGPT prepares a remediation pull request that can include:

1. HorizontalPodAutoscaler changes for workload saturation.
2. Resource request and limit updates for CPU or memory pressure.
3. Retry policies with bounded exponential backoff and jitter.
4. Circuit breakers around Redis, Kafka, PostgreSQL, feature stores, and external APIs.
5. GitOps manifests that ArgoCD can reconcile after human approval.

Each remediation should include the experiment timeline, telemetry links, root-cause summary, expected impact, rollback instructions, and ownership metadata.
