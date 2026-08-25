"""Train a deterministic, lightweight transaction-risk model for local platform demos."""
import json
from pathlib import Path
import sys

import joblib
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "services" / "inference-api"))


def build_dataset(seed: int = 42) -> tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(seed)
    n = 4_000
    amount = rng.lognormal(4.3, 1.0, n)
    frequency = rng.poisson(4, n)
    category = rng.integers(0, 6, n)
    distance = rng.exponential(80, n)
    device = rng.beta(2, 7, n)
    age = rng.integers(1, 5000, n)
    chargebacks = rng.poisson(.15, n)
    velocity = rng.poisson(2, n)
    logits = -4 + .002 * amount + .12 * frequency + .006 * distance + 4 * device - .00025 * age + 1.2 * chargebacks + .14 * velocity + .3 * (category == 4)
    probability = 1 / (1 + np.exp(-logits))
    labels = rng.binomial(1, probability)
    return np.column_stack((amount, frequency, category, distance, device, age, chargebacks, velocity)), labels


def main() -> None:
    x, y = build_dataset()
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=.2, random_state=42, stratify=y)
    model = LogisticRegression(max_iter=1000, class_weight="balanced").fit(x_train, y_train)
    artifact = ROOT / "model/artifacts/transaction-risk.joblib"
    metadata = ROOT / "model/metadata/transaction-risk.json"
    artifact.parent.mkdir(parents=True, exist_ok=True); metadata.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, artifact)
    metadata.write_text(json.dumps({"name": "transaction-risk", "version": "1.0.0", "stage": "development", "framework": "scikit-learn", "feature_count": 8, "roc_auc": round(float(roc_auc_score(y_test, model.predict_proba(x_test)[:, 1])), 4), "artifact": str(artifact.relative_to(ROOT)), "training_data": "deterministic synthetic transaction distribution", "mlflow_run_id": "local-not-tracked"}, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {artifact} and {metadata}")


if __name__ == "__main__": main()
