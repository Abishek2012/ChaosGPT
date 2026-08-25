"""Executable model promotion gate; exits non-zero on failed requirements."""
import json
import statistics
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "services" / "inference-api"))
from app.model_service import ModelService  # noqa: E402
from app.schemas import TransactionFeatures  # noqa: E402

MIN_ROC_AUC, MAX_P95_MS = .70, 50.0


def main() -> None:
    metadata_path = ROOT / "model/metadata/transaction-risk.json"
    model_path = ROOT / "model/artifacts/transaction-risk.joblib"
    required = {"name", "version", "stage", "roc_auc", "artifact", "framework"}
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    missing = required - metadata.keys()
    if missing or metadata["roc_auc"] < MIN_ROC_AUC: raise SystemExit(f"validation failed: missing={sorted(missing)} roc_auc={metadata.get('roc_auc')}")
    service = ModelService.load(model_path, metadata_path)
    sample = TransactionFeatures(transaction_amount=123.45, transaction_frequency_24h=3, merchant_category="electronics", geographic_distance_km=14, device_risk_score=.2, account_age_days=850, previous_chargebacks=0, velocity_1h=1)
    timings = []
    for _ in range(100):
        start = time.perf_counter(); service.predict(sample); timings.append((time.perf_counter() - start) * 1000)
    p95 = statistics.quantiles(timings, n=20)[18]
    if p95 > MAX_P95_MS: raise SystemExit(f"validation failed: p95_ms={p95:.3f} > {MAX_P95_MS}")
    print(f"promotion gate passed: roc_auc={metadata['roc_auc']}, p95_ms={p95:.3f}, artifact_valid=true")


if __name__ == "__main__": main()
