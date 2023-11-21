# Home

## Overview

This chart deploys all home resources in one install using the (flux-core helm chart)[https://github.com/awalford16/charts/tree/master/flux-core]. 

Values files are defined in config maps which are referenced by the flux-core chart when creating HelmReleases.


## Manual Deployment

To manually deploy the resources, simply run `helm install home .` from the chart directory. Providing the cluster is running Flux then it will install components defined in the values file.


## GitOps

Reference README in the `core/` directory to understand how the GitOps deployment works. Instead of having to run `helm upgrade` each time values change, this can be managed by Flux itself when new changes to this chart are pushed to the master branch.
