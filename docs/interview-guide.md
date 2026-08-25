# Interview guide

**Why Kubernetes and GitOps?** Kubernetes gives scheduling, probes, rollouts and portable resource controls for an inference API. GitOps makes reviewed desired state the deployment authority; Argo reconciles drift, so CI need not possess cluster mutation credentials.

**How is a bad model handled?** A candidate must pass artifact/metadata, ROC-AUC and latency gates. Production is an immutable image plus registered model version; rollback pins the prior GitOps tag and MLflow alias, then validates readiness and SLOs.

**How is cost per inference calculated?** In a cluster, OpenCost allocation is divided by Prometheus inference count over the same window. Locally `/cost` exposes its configured request-rate estimate and labels it as such. I inspect utilization percentiles before right-sizing.

**Why HPA and KEDA?** HPA responds to sustained resource demand; request/queue signals better represent service pressure. KEDA is appropriate for event-driven bursts. Both must be bounded by latency/SLO and cost telemetry.

**How do you run chaos safely?** Write a hypothesis, baseline golden signals, scope selector/duration/blast radius, require approval, run outside production, measure recovery and error-budget impact, and stop/delete the experiment if guardrails breach.

**How do you debug high p95?** Correlate request rate, model latency histogram, CPU throttling, memory, GC/logs/traces, replica count and downstream dependencies. Scale/optimize only after locating the saturation point.

**How would you handle 10x/multi-region/drift?** Load-test and set queue/request scaling, warm model replicas and use regional GitOps overlays. Replicate artifacts and use global routing. Detect feature/prediction distribution change, then evaluate a retrained candidate through the same gates.
