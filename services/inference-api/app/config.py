from dataclasses import dataclass
from pathlib import Path
import os


@dataclass(frozen=True)
class Settings:
    model_path: Path = Path(os.getenv("MODEL_PATH", "model/artifacts/transaction-risk.joblib"))
    metadata_path: Path = Path(os.getenv("MODEL_METADATA_PATH", "model/metadata/transaction-risk.json"))
    model_stage: str = os.getenv("MODEL_VERSION", "development")
    cpu_hourly_usd: float = float(os.getenv("CPU_HOURLY_USD", "0.031611"))
    memory_gib_hourly_usd: float = float(os.getenv("MEMORY_GIB_HOURLY_USD", "0.004237"))
    slo_target: float = float(os.getenv("SLO_TARGET", "0.999"))
