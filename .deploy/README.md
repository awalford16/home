# Deploy an Environment

Each Yaml file in this directory represents an environment. It will install a collection of applications using the flux-core helm chart.

## Install

```
helm repo add awalford16 https://awalford16.github.io/helm_charts
helm install core awalford16/flux-core -f home.yaml
```

This will deploy a collection of HelmRelease resources defined in the yaml file to a kubernetes cluster and install the relevant applications.


## App of Apps

To remove the need to manually apply changes to helm releases, GitOps can be used to deploy the core release itself so new applications can be easily added. The `bootstrap.yaml` file creates a Kustomization deployment which will monitor a ConfigMap resource which defines the values used in the `flux-core` helm release.

New commits to the `apps.yaml` config map will be picked up by the bootstrap release, update the config map in the cluster and in turn update the core HelmRelease to deploy applications defined in the values.
