# Home

## Deployment

This chart deploys all home resources in one install using the (flux-core helm chart)[https://github.com/awalford16/charts/tree/master/flux-core]. 

Values files are defined in config maps which are referenced by the flux-core chart when creating HelmReleases.
