# Security controls

The image runs as UID 10001 with dropped capabilities, read-only root filesystem, RuntimeDefault seccomp, no mounted service-account token, resource bounds, and probes. Helm includes a default-deny NetworkPolicy; production must enumerate ingress/egress dependencies. Kyverno audits immutable tags, non-root execution, and resources. CI creates an SBOM, scans with Trivy, and keylessly signs the immutable image with Cosign.

Secrets are injected from a Kubernetes Secret only as a local pattern. Production should use External Secrets plus a cloud/KMS-backed secret manager, admission signature verification, protected GitOps branches, and least-privilege Argo projects.
