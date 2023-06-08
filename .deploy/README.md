# Deploy an Environment

Each Yaml file in this directory represents an environment. It will install a collection of applications using the flux-core helm chart.

## Install

```
helm repo add awalford16 https://awalford16.github.io/helm_charts
helm install core awalford16/flux-core -f home.yaml
```

This will deploy a collection of HelmRelease resources defined in the yaml file to a kubernetes cluster and install the relevant applications.


