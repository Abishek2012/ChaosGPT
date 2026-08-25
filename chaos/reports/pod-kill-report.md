# Pod-kill experiment report

- **Status:** template — no experiment has been executed by this repository.
- **Hypothesis:** one inference pod can fail without breaching the service SLO.
- **Blast radius:** one labelled pod in `ml-platform`, 30 seconds, disposable cluster only.
- **Steady state:** availability ___; p95 ___ ms; replicas ___; estimated/OpenCost allocation ___.
- **Actual during failure:** availability ___; p95 ___ ms; error rate ___; replicas ___; cost ___.
- **Recovery:** pod recovery time ___ seconds; rollback is `kubectl delete -f chaos/experiments/pod-kill.yaml`.
- **Conclusion:** pending measured experiment.
