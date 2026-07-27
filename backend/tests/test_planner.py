import pytest
from app.application.planner import DeterministicSafetyPlanner
from app.domain.models import FailureMode

def test_black_friday_plan_is_policy_guarded():
    plan = DeterministicSafetyPlanner().plan("Simulate Black Friday", "production-canary", 5)
    assert plan.blast_radius.require_approval is True
    assert plan.blast_radius.max_customer_impact_percent == 5
    assert [step.failure_mode for step in plan.steps] == [FailureMode.LATENCY, FailureMode.POD_KILL, FailureMode.PACKET_LOSS, FailureMode.POSTGRES_FAILURE]

def test_unsupported_intent_is_rejected():
    with pytest.raises(ValueError):
        DeterministicSafetyPlanner().plan("delete everything", "default")
