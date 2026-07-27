package main

import (
	"encoding/json"
	"fmt"
	"os"
)

type ExperimentPlan struct {
	Scenario               string   `json:"scenario"`
	Namespace              string   `json:"namespace"`
	MaxCustomerImpact      int      `json:"maxCustomerImpactPercent"`
	Actions                []string `json:"actions"`
	RemediationPullRequest bool     `json:"remediationPullRequest"`
}

func main() {
	plan := ExperimentPlan{
		Scenario:               "black_friday",
		Namespace:              "production-canary",
		MaxCustomerImpact:      5,
		Actions:                []string{"pod-kill", "network-latency", "redis-packet-loss", "postgres-throttle"},
		RemediationPullRequest: true,
	}

	encoder := json.NewEncoder(os.Stdout)
	encoder.SetIndent("", "  ")
	if err := encoder.Encode(plan); err != nil {
		fmt.Fprintf(os.Stderr, "encode plan: %v\n", err)
		os.Exit(1)
	}
}
