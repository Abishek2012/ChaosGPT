import json
import urllib.request

base = "http://127.0.0.1:8080"
payload = {"transaction_amount": 120.5, "transaction_frequency_24h": 2, "merchant_category": "grocery", "geographic_distance_km": 4, "device_risk_score": .1, "account_age_days": 900, "previous_chargebacks": 0, "velocity_1h": 1}
for path in ("/health", "/ready", "/cost"):
    with urllib.request.urlopen(base + path, timeout=5) as response: print(path, response.status)
request = urllib.request.Request(base + "/predict", data=json.dumps(payload).encode(), headers={"Content-Type": "application/json"}, method="POST")
with urllib.request.urlopen(request, timeout=5) as response: print("/predict", response.status, json.load(response)["risk_classification"])
