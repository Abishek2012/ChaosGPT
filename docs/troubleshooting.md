# Troubleshooting

- `503 /ready`: run `make train`; inspect artifact and metadata paths.
- HPA remains unknown: install metrics-server and Prometheus Adapter; `kubectl describe hpa` shows missing metrics.
- Pod will not start: inspect `kubectl describe pod`; common causes are image availability, read-only filesystem writes, or failing startup probe.
- No cost data: verify OpenCost scrape and use the same time window as `aegisml_inferences_total`; local `/cost` is an estimate only.
- Chaos experiment has no effect: confirm Chaos Mesh is installed and that the target pod has the `aegisml.io/chaos-approved=true` label.
