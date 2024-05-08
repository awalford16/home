"""A Linode Python Pulumi program"""

import pulumi
import pulumi_linode
import inventory
import os

from pathlib import Path
from pulumi_command import local

SSH_FILE_PATH = os.environ.get("SSH_FILE_PATH", f"{str(Path.home())}/.ssh/id_ed25519.pub")

ssh_file = open(SSH_FILE_PATH, "r")
ssh_key = ssh_file.readline().replace("\n", "")
stack_name = pulumi.get_stack()

config = pulumi.Config()

# Define inventoary file for access via Ansible
inventory_file = os.path.join(os.path.dirname(__file__), "inventory.ini")

instances = []
for i in range(config.get_int("worker_nodes") + 1):
    id = f"worker-{i}"

    # Always create master node
    if i == 0:
        id = "master"

    # Create a Linode resource (Linode Instance)
    instances.append(pulumi_linode.Instance(
        f"k3s-{stack_name}-{id}",
        authorized_keys=[ssh_key],
        type="g6-nanode-1",
        region="eu-west",
        label=f"{stack_name}-{id}",
        image="linode/ubuntu22.04",
    ))

    # Export the Instance label of the instance
    pulumi.export(f"instance_{i}_label", instances[i].label)
    pulumi.export(f"instance_{i}_ip", instances[i].ip_address)


# Write to inventory file and workers group_vars with master IP address
pulumi.Output.all(*[i.ip_address for i in instances]).apply(
    lambda ip: inventory.create_inventory(
        template_file="inventory.ini.tpl", destination=inventory_file, ip_address=f"{ip[0]}", workers=[f"{worker}" for worker in ip[1:]]
    )
)
