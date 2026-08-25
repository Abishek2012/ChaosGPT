PYTHON ?= python3
VENV ?= .venv
PY := $(VENV)/bin/python
PIP := $(VENV)/bin/pip
IMAGE ?= ghcr.io/example/aegisml-inference
IMAGE_TAG ?= dev-$(shell git rev-parse --short HEAD 2>/dev/null || echo local)

.PHONY: setup test lint train validate-model run build setup-cluster deploy destroy chaos finops dashboards smoke-test
setup:
	$(PYTHON) -m venv $(VENV)
	$(PIP) install -r services/inference-api/requirements.txt -r services/inference-api/requirements-dev.txt
test:
	$(PY) -m pytest services/inference-api/tests ml/validation/tests
lint:
	$(PY) -m ruff check services/inference-api/app ml finops
train:
	$(PY) ml/training/train.py
validate-model:
	$(PY) ml/validation/validate_model.py
run:
	PYTHONPATH=services/inference-api $(PY) -m uvicorn app.main:app --host 127.0.0.1 --port 8080
build:
	docker build -f services/inference-api/Dockerfile -t $(IMAGE):$(IMAGE_TAG) .
setup-cluster:
	scripts/kind-up.sh
	for n in ml-platform monitoring chaos finops; do kubectl create namespace $$n --dry-run=client -o yaml | kubectl apply -f -; done
deploy:
	helm upgrade --install aegisml helm/inference-service --namespace ml-platform --create-namespace --set image.repository=$(IMAGE) --set image.tag=$(IMAGE_TAG)
destroy:
	helm uninstall aegisml --namespace ml-platform || true
	kind delete cluster --name aegisml || true
chaos:
	kubectl apply -f chaos/experiments/pod-kill.yaml
finops:
	PYTHONPATH=services/inference-api $(PY) finops/recommendations/generate.py
dashboards:
	echo 'Import observability/grafana/dashboards/aegisml-platform.json into Grafana.'
smoke-test:
	PYTHONPATH=services/inference-api $(PY) scripts/smoke_test.py
