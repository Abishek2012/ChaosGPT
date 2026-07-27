from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from app.application.planner import DeterministicSafetyPlanner
from app.infrastructure.kubernetes_discovery import KubernetesDiscoveryService

app = FastAPI(title="ChaosGPT Control Plane", version="1.0.0")
planner = DeterministicSafetyPlanner()

class PlanRequest(BaseModel):
    intent: str = Field(min_length=3)
    namespace: str = Field(min_length=1)
    max_customer_impact_percent: int = Field(default=5, ge=0, le=100)

@app.get("/healthz")
async def healthz() -> dict[str, str]:
    return {"status": "ok"}

@app.post("/api/v1/experiments/plans")
async def create_plan(request: PlanRequest) -> dict:
    try:
        plan = planner.plan(request.intent, request.namespace, request.max_customer_impact_percent)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return {
        "title": plan.title,
        "intent": plan.intent,
        "status": plan.status,
        "blast_radius": plan.blast_radius.__dict__,
        "steps": [{**step.__dict__, "failure_mode": step.failure_mode.value} for step in plan.steps],
    }

@app.get("/api/v1/clusters/local/inventory")
async def cluster_inventory() -> dict:
    inventory = await KubernetesDiscoveryService().discover()
    return inventory.__dict__
