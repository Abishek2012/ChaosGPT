# MLOps lifecycle

`ml/training/train.py` produces a deterministic synthetic transaction model and metadata. Production training logs parameters, metrics, artifacts and registry versions to MLflow. `ml/validation/validate_model.py` blocks a candidate without required metadata, a valid joblib artifact, ROC-AUC ≥ 0.70, or p95 local prediction latency ≤ 50 ms. The test model is deliberately lightweight: operational maturity, not accuracy, is the project focus.

Promotion is development, staging, then production. A production rollout records the MLflow version and immutable image digest; a bad model rolls back both the GitOps tag and MLflow alias. Monitor probability distributions and feature summaries for drift; investigate and retrain rather than silently auto-promoting.
