# DevSecOps pipeline

The workflow runs lint, API/model tests, executable validation gates, SBOM generation, image build/push, Trivy HIGH/CRITICAL scan, and Cosign signing. Only after those steps it commits a SHA tag to GitOps. Argo performs reconciliation; no CI `kubectl apply` exists. A production workflow should separate the GitOps repository and use pull requests/approved environments rather than enabling CI to push directly to protected branches.
