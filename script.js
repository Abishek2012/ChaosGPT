const scenarios = {
  blackFriday: {
    name: 'Black Friday traffic readiness',
    intent: 'Protect checkout, recommendations, payments, and Redis-backed sessions during a 12x traffic spike.',
    actions: [
      'Scale synthetic load from 1x to 12x over 15 minutes',
      'Inject 220ms p95 latency into checkout and catalog services',
      'Kill 25% of checkout pods after cart traffic peaks',
      'Restart one worker node in the recommendation pool',
      'Add 3% packet loss between API gateway and Redis',
      'Throttle PostgreSQL writes for order creation for 4 minutes'
    ],
    fixes: ['Tune HPA target CPU to 55%', 'Add Redis circuit breaker', 'Increase checkout retry budget with jitter']
  },
  modelDrift: {
    name: 'Model drift recovery',
    intent: 'Verify that an inference service detects drift, falls back safely, and preserves SLOs under degraded feature quality.',
    actions: [
      'Replay skewed feature payloads into the inference API',
      'Inject 400ms latency into the feature-store dependency',
      'Kill one model-serving pod during canary promotion',
      'Force stale cache reads for 6 minutes',
      'Trigger alert routing for accuracy and p99 latency budgets'
    ],
    fixes: ['Add drift guardrail threshold', 'Promote shadow-model rollback policy', 'Cache high-value features locally']
  },
  regionalOutage: {
    name: 'Regional cloud outage',
    intent: 'Exercise multi-cloud failover across Kubernetes clusters and managed data services.',
    actions: [
      'Deny egress to one cloud region for customer APIs',
      'Delete a non-critical ConfigMap to test GitOps reconciliation',
      'Fill disk on one logging node to 90%',
      'Inject DNS failures for 120 seconds',
      'Validate Terraform drift detection after recovery'
    ],
    fixes: ['Add regional failover runbook', 'Harden DNS retry strategy', 'Add log-volume autoscaling policy']
  }
};

const failureModes = [
  'Kill Pods', 'Kill Nodes', 'Delete PVCs', 'Delete ConfigMaps', 'Network Latency', 'Packet Loss',
  'CPU Stress', 'Memory Stress', 'Disk Fill', 'DNS Failure', 'API Failure', 'Kafka Failure',
  'Redis Failure', 'PostgreSQL Failure', 'Feature Store Latency', 'Model Drift', 'Canary Rollback', 'Pipeline Retry'
];

const planOutput = document.querySelector('#plan-output');
const scenarioSelect = document.querySelector('#scenario-select');
const generatePlanButton = document.querySelector('#generate-plan');
const failureGrid = document.querySelector('#failure-grid');

function renderFailureCatalog() {
  failureGrid.innerHTML = failureModes
    .map((mode) => `<span class="failure-pill">${mode}</span>`)
    .join('');
}

function renderPlan(key = 'blackFriday') {
  const scenario = scenarios[key];
  const actions = scenario.actions.map((action) => `  - ${action}`).join('\n');
  const fixes = scenario.fixes.map((fix) => `  - ${fix}`).join('\n');

  planOutput.textContent = `scenario: ${scenario.name}\nintent: ${scenario.intent}\nblast_radius:\n  namespace: production-canary\n  max_customer_impact: 5%\nactions:\n${actions}\nobservability:\n  - Prometheus SLO burn rate\n  - Loki error burst detection\n  - Tempo trace waterfall\n  - OpenTelemetry dependency map\nai_outputs:\n  rca: generated after experiment\n  timeline: generated from events and spans\n  suggested_fixes:\n${fixes}\n  github_pr: terraform-and-k8s-remediation`;
}

generatePlanButton.addEventListener('click', () => renderPlan(scenarioSelect.value));
scenarioSelect.addEventListener('change', () => renderPlan(scenarioSelect.value));

renderFailureCatalog();
renderPlan();
