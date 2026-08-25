from pathlib import Path
import sys

from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "services" / "inference-api"))
from app.main import app
from ml.training.train import main as train


def test_prediction_and_operational_endpoints():
    train()
    with TestClient(app) as client:
        assert client.get("/health").status_code == 200
        assert client.get("/ready").status_code == 200
        response = client.post("/predict", json={"transaction_amount": 900, "transaction_frequency_24h": 4, "merchant_category": "travel", "geographic_distance_km": 800, "device_risk_score": .7, "account_age_days": 30, "previous_chargebacks": 1, "velocity_1h": 5})
        assert response.status_code == 200
        assert response.json()["risk_classification"] in {"low", "medium", "high"}
        assert client.get("/cost").json()["cost_basis"].startswith("estimated")
