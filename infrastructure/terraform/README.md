# Terraform foundation

The module boundary separates cluster, network, object storage, observability, and database concerns. Backends and credentials are supplied by each environment; no secrets are committed. Configure a remote state backend with locking before applying a cloud environment.
