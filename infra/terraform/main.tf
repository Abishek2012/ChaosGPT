terraform {
  required_version = ">= 1.6.0"
}

variable "environment" {
  description = "Environment name for ChaosGPT resources."
  type        = string
  default     = "dev"
}

output "chaosgpt_environment" {
  value = var.environment
}
