variable "environment" { type = string }
variable "tags" { type = map(string) default = {} }

# Provider-specific EKS/AKS/GKE, bucket, and PostgreSQL resources implement this
# contract in a cloud environment. Keeping this root free of provider resources
# preserves an intentionally portable platform interface.
output "environment" { value = var.environment }
output "required_components" { value = ["network", "kubernetes", "object-storage", "postgresql", "observability"] }
