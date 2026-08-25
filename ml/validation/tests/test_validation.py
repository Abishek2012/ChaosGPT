from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "ml" / "training"))
from train import build_dataset


def test_synthetic_training_data_has_expected_shape():
    features, labels = build_dataset()
    assert features.shape == (4000, 8)
    assert set(labels) <= {0, 1}
