# Infra

The Infra directory is designed for setting up test infrastructure using Pulumi and Ansible.

A Linode token is required to provision the VMs. The make commands will assume a token is stored under `~/.linode` or can be passed directly to the make command with `make infra LINODE_TOKEN=...`

## Pulumi

The Pulumi stage will provision small VMs in Linode adding an SSH key from `~/.ssh/id_ed25519.pub`

It can be triggered by running `make nodes`

Using the IP address of the newly created node, an inventory.ini file will be generated from the one found in the `templates/` directory. 


## Ansible

Using the inventory generated from the previous stage, the Ansible is responsible for installing k3s onto the nodes.

It can be run with `make ansible`

The Ansible will copy the Kube config file across from the k3s host onto the local machine with the relevant values patched and saved to `~/.kube/STACK.yaml` where `STACK` is the name of the pulumi stack.

## Bootstrap

The Bootstrap stage is another Pulumi run to install Flux onto the k3s cluster and register the cluster with this github repo. This will allow tools required for the cluster to be installed onto the cluster.

It can be triggered with `make bootstrap`
