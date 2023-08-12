# Core

## Overview

This is the bootstrapping directory of the cluster. The `core.yaml` file defines the values for the flux-core chart. This will tell Flux to watch GitHub with the latest changes to this repository.

Core is configured to point at `.deploy/home` in master which will define the applications to install. As the values are updated in the home directory and pushed to master to update/deploy applications, Flux will detect these changes and sync accordingly.

## Cluster Setup

The cluster should be setup with Flux. Intall command for new clusters:

```
flux bootstrap github --personal --owner awalford16 --repository home --path=clusters/CLUSTER_NAME
```
