import logging
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import Response
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest

from app.config import Settings
from app.cost import CostSnapshot
from app.metrics import CONFIDENCE, ERRORS, INFERENCES, LATENCY, MODEL_INFO, REQUESTS
from app.model_service import ModelService
from app.schemas import Prediction, TransactionFeatures

logging.basicConfig(format="%(asctime)s %(levelname)s %(name)s %(message)s", level=logging.INFO)
logger = logging.getLogger("aegisml.inference")
settings = Settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        app.state.model_service = ModelService.load(settings.model_path, settings.metadata_path)
        metadata = app.state.model_service.metadata
        MODEL_INFO.labels(metadata["version"], settings.model_stage).set(1)
        app.state.ready = True
        app.state.started_at = time.monotonic()
        app.state.inferences = 0
        logger.info("model_loaded version=%s", metadata["version"])
    except Exception as exc:
        app.state.ready = False
        logger.exception("model_load_failed error=%s", exc)
    yield


app = FastAPI(title="AegisML Transaction Risk API", version="1.0.0", lifespan=lifespan)


@app.middleware("http")
async def instrument(request: Request, call_next):
    response = await call_next(request)
    REQUESTS.labels(request.method, request.url.path, str(response.status_code)).inc()
    return response


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/ready")
def ready() -> dict[str, str]:
    if not app.state.ready:
        raise HTTPException(503, "model is not ready")
    return {"status": "ready"}


@app.get("/metrics")
def metrics() -> Response:
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.post("/predict", response_model=Prediction)
def predict(features: TransactionFeatures) -> Prediction:
    if not app.state.ready:
        raise HTTPException(503, "model is not ready")
    try:
        prediction = app.state.model_service.predict(features)
        app.state.inferences += 1
        INFERENCES.labels(prediction.model_version, prediction.risk_classification).inc()
        LATENCY.labels(prediction.model_version).observe(prediction.inference_latency_ms / 1000)
        CONFIDENCE.observe(prediction.risk_probability)
        return prediction
    except Exception as exc:
        ERRORS.labels("prediction_failure").inc()
        logger.exception("prediction_failed")
        raise HTTPException(500, "inference failed") from exc


@app.get("/model")
def model() -> dict:
    return app.state.model_service.metadata if app.state.ready else {"status": "unavailable"}


@app.get("/version")
def version() -> dict[str, str]:
    return {"service_version": app.version, "model_version": app.state.model_service.metadata["version"] if app.state.ready else "unavailable"}


@app.get("/cost")
def cost() -> dict[str, object]:
    return CostSnapshot(inferences_since_start=getattr(app.state, "inferences", 0)).estimate(settings.cpu_hourly_usd, settings.memory_gib_hourly_usd)


@app.get("/reliability")
def reliability() -> dict[str, object]:
    # Process-local counters are a local substitute; production dashboard derives this from Prometheus.
    return {"slo": "99.9% successful inference requests", "measurement": "process_local", "status": "healthy" if app.state.ready else "degraded", "error_budget_fraction": 1 - settings.slo_target}
