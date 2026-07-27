#!/usr/bin/env bash
set -euo pipefail
kind create cluster --name chaosgpt --wait 120s
kubectl create namespace chaosgpt --dry-run=client -o yaml | kubectl apply -f -
