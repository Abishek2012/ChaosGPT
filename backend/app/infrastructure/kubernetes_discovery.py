from dataclasses import dataclass

@dataclass(frozen=True)
class ClusterInventory:
    namespaces: list[str]
    deployments: list[str]
    pods: list[str]
    nodes: list[str]
    pvcs: list[str]
    services: list[str]
    ingresses: list[str]

class KubernetesDiscoveryService:
    def __init__(self, context: str | None = None) -> None:
        self.context = context

    async def discover(self) -> ClusterInventory:
        try:
            from kubernetes import client, config
        except ImportError as exc:
            raise RuntimeError("Install kubernetes package or run the Docker image with dependencies") from exc

        config.load_kube_config(context=self.context)
        core = client.CoreV1Api()
        apps = client.AppsV1Api()
        networking = client.NetworkingV1Api()
        return ClusterInventory(
            namespaces=[item.metadata.name for item in core.list_namespace().items],
            deployments=[item.metadata.name for item in apps.list_deployment_for_all_namespaces().items],
            pods=[item.metadata.name for item in core.list_pod_for_all_namespaces().items],
            nodes=[item.metadata.name for item in core.list_node().items],
            pvcs=[item.metadata.name for item in core.list_persistent_volume_claim_for_all_namespaces().items],
            services=[item.metadata.name for item in core.list_service_for_all_namespaces().items],
            ingresses=[item.metadata.name for item in networking.list_ingress_for_all_namespaces().items],
        )
