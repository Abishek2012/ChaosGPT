from dataclasses import dataclass, field
from enum import Enum

class ExperimentStatus(str, Enum):
    DRAFT = "draft"
    PENDING_APPROVAL = "pending_approval"
    APPROVED = "approved"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

class FailureMode(str, Enum):
    CPU_STRESS = "cpu_stress"
    MEMORY_STRESS = "memory_stress"
    DISK_PRESSURE = "disk_pressure"
    POD_KILL = "pod_kill"
    NODE_DRAIN = "node_drain"
    DNS_FAILURE = "dns_failure"
    PACKET_LOSS = "packet_loss"
    LATENCY = "latency"
    BANDWIDTH_THROTTLE = "bandwidth_throttle"
    REDIS_FAILURE = "redis_failure"
    KAFKA_FAILURE = "kafka_failure"
    POSTGRES_FAILURE = "postgres_failure"
    API_TIMEOUT = "api_timeout"
    PVC_DELETE = "pvc_delete"
    CONFIGMAP_DELETE = "configmap_delete"
    SECRET_DELETE = "secret_delete"

@dataclass(frozen=True)
class BlastRadius:
    namespace: str
    max_customer_impact_percent: int = 5
    require_approval: bool = True

    def __post_init__(self) -> None:
        if not self.namespace:
            raise ValueError("namespace is required")
        if not 0 <= self.max_customer_impact_percent <= 100:
            raise ValueError("max_customer_impact_percent must be between 0 and 100")

@dataclass(frozen=True)
class ExperimentStep:
    name: str
    failure_mode: FailureMode
    target: str
    duration_seconds: int
    parameters: dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.duration_seconds <= 0:
            raise ValueError("duration_seconds must be positive")

@dataclass(frozen=True)
class ExperimentPlan:
    title: str
    intent: str
    blast_radius: BlastRadius
    steps: tuple[ExperimentStep, ...]
    status: ExperimentStatus = ExperimentStatus.PENDING_APPROVAL

    def approve(self) -> "ExperimentPlan":
        return ExperimentPlan(self.title, self.intent, self.blast_radius, self.steps, ExperimentStatus.APPROVED)
