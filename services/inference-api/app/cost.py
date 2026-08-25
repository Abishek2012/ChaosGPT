from dataclasses import dataclass


@dataclass(frozen=True)
class CostSnapshot:
    replicas: int = 2
    cpu_cores_requested: float = 0.5
    memory_gib_requested: float = 0.5
    inferences_since_start: int = 0

    def estimate(self, cpu_hourly_usd: float, memory_gib_hourly_usd: float) -> dict[str, object]:
        hourly = self.replicas * (self.cpu_cores_requested * cpu_hourly_usd + self.memory_gib_requested * memory_gib_hourly_usd)
        count = max(self.inferences_since_start, 1)
        return {"cost_basis": "estimated_from_configured_local_unit_rates", "hourly_usd": round(hourly, 6), "daily_usd": round(hourly * 24, 4), "monthly_usd": round(hourly * 24 * 30, 2), "cost_per_inference_usd": round(hourly / count, 8), "cost_per_1000_inferences_usd": round(hourly * 1000 / count, 6), "inference_count_window": self.inferences_since_start, "measured_open_cost_data": False}
