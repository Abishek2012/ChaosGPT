from prometheus_client import Counter, Histogram, Gauge

REQUESTS = Counter("aegisml_http_requests_total", "HTTP requests", ["method", "path", "status"])
INFERENCES = Counter("aegisml_inferences_total", "Completed inferences", ["model_version", "classification"])
ERRORS = Counter("aegisml_inference_errors_total", "Inference errors", ["reason"])
LATENCY = Histogram("aegisml_inference_latency_seconds", "Inference latency", ["model_version"], buckets=(.001, .005, .01, .025, .05, .1, .25, .5, 1, 2))
CONFIDENCE = Histogram("aegisml_prediction_probability", "Predicted fraud probability", buckets=(0, .1, .25, .5, .75, .9, 1))
MODEL_INFO = Gauge("aegisml_model_info", "Active model metadata", ["version", "stage"])
