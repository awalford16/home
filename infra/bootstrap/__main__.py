import pulumi
import pulumi_github as github
import pulumi_tls as tls
import pulumi_flux as flux
from pygit2 import Repository

import os

# Require Github configurations
# export GITHUB_TOKEN=your-github-personal-access-token
# export GITHUB_OWNER=your-github-owner

stack_name = pulumi.get_stack()
config = pulumi.Config()

GITHUB_REPO = os.environ.get("GITHUB_REPO", "home")
GITHUB_OWNER = os.environ.get("GITHUB_OWNER", config.get("github:owner"))
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")

branch = Repository('.').head.shorthand
target_path = f"clusters/{stack_name}"

ssh_key = tls.PrivateKey("key", algorithm="ECDSA", ecdsa_curve="P256")
provider = flux.Provider(
    "flux",
    kubernetes=flux.ProviderKubernetesArgs(config_path=f"~/.kube/{stack_name}"),
    git=flux.ProviderGitArgs(
        url=f"ssh://git@github.com/{GITHUB_OWNER}/{GITHUB_REPO}.git",
        branch=branch,
        ssh=flux.ProviderGitSshArgs(username="git", private_key=ssh_key.private_key_pem)
    )
)

deploy_key = github.RepositoryDeployKey(
    "flux-key",
    title=f"{stack_name}-bootstrap",
    repository=GITHUB_REPO,
    key=ssh_key.public_key_openssh,
    read_only=False,
)

resource = flux.FluxBootstrapGit(
    "flux",
    path=target_path,
    opts=pulumi.ResourceOptions(provider=provider, depends_on=deploy_key)
)
