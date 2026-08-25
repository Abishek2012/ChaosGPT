#!/usr/bin/env bash
set -euo pipefail
kind create cluster --name aegisml --wait 120s
for namespace in ml-platform monitoring chaos finops; do
  kubectl create namespace "$namespace" --dry-run=client -o yaml | kubectl apply -f -
done
