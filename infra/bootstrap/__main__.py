import pulumi
import pulumi_github as github
import pulumi_tls as tls
import pulumi_flux as flux
import pulumi_kubernetes as kubernetes
from pulumi_kubernetes.helm.v3 import Chart, ChartOpts, FetchOpts

from pygit2 import Repository

import os
import yaml

# Require Github configurations
# export GITHUB_TOKEN=your-github-personal-access-token
# export GITHUB_OWNER=your-github-owner

stack_name = pulumi.get_stack()
config = pulumi.Config()

GITHUB_REPO = os.environ.get("GITHUB_REPO", "home")
GITHUB_OWNER = os.environ.get("GITHUB_OWNER", config.get("github:owner"))
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")

# ../../.deploy
default_bootstrap_values_path = os.path.abspath(os.path.join(os.getcwd(), os.path.pardir, os.path.pardir, ".deploy"))
BOOTSTRAP_VALUES = os.environ.get("BOOTSTRAP_VALUES", default_bootstrap_values_path)

branch = Repository('.').head.shorthand
target_path = f"clusters/{stack_name}"

ssh_key = tls.PrivateKey("key", algorithm="ECDSA", ecdsa_curve="P256")
flux_provider = flux.Provider(
    "flux",
    kubernetes=flux.ProviderKubernetesArgs(config_path=f"~/.kube/{stack_name}"),
    git=flux.ProviderGitArgs(
        url=f"ssh://git@github.com/{GITHUB_OWNER}/{GITHUB_REPO}.git",
        branch=branch,
        ssh=flux.ProviderGitSshArgs(username="git", private_key=ssh_key.private_key_pem)
    )
)

kube_provider = kubernetes.Provider(
    "kube",
    kubeconfig=f"{os.path.expanduser('~')}/.kube/{stack_name}",
    context=stack_name
)

deploy_key = github.RepositoryDeployKey(
    "flux-key",
    title=f"{stack_name}-bootstrap",
    repository=GITHUB_REPO,
    key=ssh_key.public_key_openssh,
    read_only=False,
)

cluster_bootstrap = flux.FluxBootstrapGit(
    "flux",
    path=target_path,
    opts=pulumi.ResourceOptions(provider=flux_provider, depends_on=deploy_key)
)

with open(f"{BOOTSTRAP_VALUES}/core.yaml") as f:
    data = yaml.full_load(f)
    
    namespace = kubernetes.core.v1.Namespace(
        "bootstrap",
        opts=pulumi.ResourceOptions(provider=kube_provider, depends_on=[cluster_bootstrap])
    )

    bootstrap = Chart(
        "bootstrap",
        ChartOpts(
            chart="flux-core",
            version="0.0.4",
            namespace=namespace.id,
            fetch_opts=FetchOpts(
                repo="https://awalford16.github.io/charts",
            ),
            values=data
        ),
        opts=pulumi.ResourceOptions(provider=kube_provider, depends_on=[cluster_bootstrap, namespace])
    )
