"""Generate conservative, data-labelled FinOps recommendations from a JSON observation."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
observation_path = ROOT / "finops/reports/observed-utilization.json"
output_path = ROOT / "finops/reports/recommendations.json"


def recommend(observation: dict[str, float]) -> list[dict[str, str]]:
    output = []
    cpu_ratio = observation["cpu_request_cores"] / max(observation["cpu_observed_cores"], .001)
    if cpu_ratio >= 1.5:
        output.append({"type": "cpu_overrequest", "evidence": f"request is {cpu_ratio:.1f}x observed average", "action": "Validate p95 usage and lower CPU request gradually; retain burst headroom."})
    if observation["replica_utilization_pct"] < 20 and observation["min_replicas"] > 1:
        output.append({"type": "idle_replicas", "evidence": f"average replica utilization is {observation['replica_utilization_pct']:.1f}%", "action": "Test lowering minReplicas while preserving the availability SLO."})
    return output


def main() -> None:
    if not observation_path.exists():
        raise SystemExit("No observation file. Export measured Prometheus/OpenCost values to finops/reports/observed-utilization.json first.")
    observation = json.loads(observation_path.read_text())
    output_path.write_text(json.dumps({"input_kind": "measured_export_supplied_by_operator", "recommendations": recommend(observation)}, indent=2) + "\n")
    print(f"wrote {output_path}")


if __name__ == "__main__": main()
