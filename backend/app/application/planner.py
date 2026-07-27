from app.domain.models import BlastRadius, ExperimentPlan, ExperimentStep, FailureMode

class DeterministicSafetyPlanner:
    """Policy-first planner used before optional LLM expansion."""

    def plan(self, intent: str, namespace: str, max_impact: int = 5) -> ExperimentPlan:
        normalized = intent.lower().strip()
        radius = BlastRadius(namespace=namespace, max_customer_impact_percent=max_impact)
        if "black friday" in normalized:
            return ExperimentPlan(
                title="Black Friday resilience validation",
                intent=intent,
                blast_radius=radius,
                steps=(
                    ExperimentStep("checkout-latency", FailureMode.LATENCY, "service/checkout", 300, {"latency_ms": "220"}),
                    ExperimentStep("checkout-pod-kill", FailureMode.POD_KILL, "deployment/checkout", 60, {"percentage": "25"}),
                    ExperimentStep("redis-packet-loss", FailureMode.PACKET_LOSS, "service/redis", 180, {"loss_percent": "3"}),
                    ExperimentStep("orders-postgres-timeout", FailureMode.POSTGRES_FAILURE, "service/postgres", 120, {"timeout_ms": "750"}),
                ),
            )
        if "drift" in normalized or "model" in normalized:
            return ExperimentPlan(
                title="Model reliability validation",
                intent=intent,
                blast_radius=radius,
                steps=(
                    ExperimentStep("feature-store-latency", FailureMode.LATENCY, "service/feature-store", 240, {"latency_ms": "400"}),
                    ExperimentStep("inference-pod-kill", FailureMode.POD_KILL, "deployment/model-server", 60, {"percentage": "20"}),
                    ExperimentStep("api-timeout", FailureMode.API_TIMEOUT, "service/inference-api", 120, {"timeout_ms": "1000"}),
                ),
            )
        raise ValueError("unsupported intent; provide a supported production scenario")
