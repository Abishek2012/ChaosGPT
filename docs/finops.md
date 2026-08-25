# FinOps methodology

OpenCost is the source for Kubernetes allocation/idle cost in a cluster. The `/cost` endpoint is a transparent **local estimate**: requested CPU/memory × configured local rates divided by in-process inference count. It does not claim to be measured billing. Grafana combines OpenCost, kube-state-metrics, cAdvisor, and application counters for namespace/workload cost, request-vs-usage, idle allocation, cost/inference and monthly projection.

`make finops` accepts an operator-exported observation JSON and emits only evidence-supported recommendations. It distinguishes measured input from calculated estimates and never invents cloud invoice data. Tune requests only after examining p95/p99 and preserving the 99.9% successful-request SLO.
