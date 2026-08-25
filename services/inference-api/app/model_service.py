import json
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import joblib
import numpy as np

from app.schemas import Prediction, TransactionFeatures

CATEGORIES = {"grocery": 0, "travel": 1, "gaming": 2, "electronics": 3, "cash_withdrawal": 4, "other": 5}


@dataclass
class ModelService:
    model: Any
    metadata: dict[str, Any]

    @classmethod
    def load(cls, model_path: Path, metadata_path: Path) -> "ModelService":
        if not model_path.is_file() or not metadata_path.is_file():
            raise FileNotFoundError("model artifact and metadata must both be present")
        with metadata_path.open(encoding="utf-8") as handle:
            metadata = json.load(handle)
        return cls(joblib.load(model_path), metadata)

    def predict(self, item: TransactionFeatures) -> Prediction:
        started = time.perf_counter()
        vector = np.array([[item.transaction_amount, item.transaction_frequency_24h, CATEGORIES[item.merchant_category], item.geographic_distance_km, item.device_risk_score, item.account_age_days, item.previous_chargebacks, item.velocity_1h]])
        probability = float(self.model.predict_proba(vector)[0][1])
        classification = "high" if probability >= .75 else "medium" if probability >= .35 else "low"
        return Prediction(risk_probability=round(probability, 6), risk_classification=classification, model_version=str(self.metadata["version"]), inference_latency_ms=round((time.perf_counter() - started) * 1000, 3))
