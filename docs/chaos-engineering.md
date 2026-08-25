# Chaos engineering

All experiments are opt-in and run only in a disposable environment. `chaos/experiments/pod-kill.yaml` kills one explicitly labelled inference pod for 30 seconds. Hypothesis: with two replicas, readiness gates, PDB, and a Service, one pod loss should preserve the 99.9% success SLO while the controller restores desired replicas.

Before: record request rate, p95, error rate, replicas and OpenCost allocation. During: apply the manifest while generating traffic. After: delete the experiment, verify ready replicas and record recovery time. Populate `chaos/reports/pod-kill-report.md` with actual observed values; blank fields are deliberate rather than simulated evidence. For network latency/loss, CPU/memory stress, and dependency failure, create separately approved Chaos Mesh manifests with the same bounded selector and report format. Never run automatically or in production.
