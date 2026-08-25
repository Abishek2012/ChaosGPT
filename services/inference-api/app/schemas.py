from typing import Literal
from pydantic import BaseModel, Field


class TransactionFeatures(BaseModel):
    transaction_amount: float = Field(ge=0, le=1_000_000)
    transaction_frequency_24h: int = Field(ge=0, le=10_000)
    merchant_category: Literal["grocery", "travel", "gaming", "electronics", "cash_withdrawal", "other"]
    geographic_distance_km: float = Field(ge=0, le=50_000)
    device_risk_score: float = Field(ge=0, le=1)
    account_age_days: int = Field(ge=0, le=100_000)
    previous_chargebacks: int = Field(ge=0, le=1000)
    velocity_1h: int = Field(ge=0, le=10_000)


class Prediction(BaseModel):
    risk_probability: float = Field(ge=0, le=1)
    risk_classification: Literal["low", "medium", "high"]
    model_version: str
    inference_latency_ms: float
