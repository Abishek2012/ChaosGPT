#!/usr/bin/env bash
set -euo pipefail
URL="${1:-http://127.0.0.1:8080/predict}"
payload='{"transaction_amount":120.5,"transaction_frequency_24h":2,"merchant_category":"grocery","geographic_distance_km":4,"device_risk_score":0.1,"account_age_days":900,"previous_chargebacks":0,"velocity_1h":1}'
while true; do curl --fail --silent --show-error -H 'content-type: application/json' -d "$payload" "$URL" >/dev/null; done
