"""A Linode Python Pulumi program"""

import pulumi
import pulumi_linode
import inventory
import os

from pathlib import Path
from pulumi_command import local

SSH_FILE_PATH = os.environ.get("SSH_FILE_PATH", f"{str(Path.home())}/.ssh/id_ed25519.pub")

ssh_file = open(SSH_FILE_PATH, "r")
stack_name = pulumi.get_stack()

### MASTER NODE
# Create a Linode resource (Linode Instance)
instance = pulumi_linode.Instance(
    f"k3s-{stack_name}-master",
    authorized_keys=[ssh_file.readline().replace("\n", "")],
    type="g6-nanode-1",
    region="eu-west",
    label=f"{stack_name}",
    image="linode/ubuntu22.04",
)

# Write to inventory file and workers group_vars with master IP address
inventory_file = os.path.join(os.path.dirname(__file__), "inventory.ini")
instance.ip_address.apply(
    lambda ip: inventory.create_inventory(
        template_file="inventory.ini.tpl", destination=inventory_file, ip_address=ip
    )
)

# Export the Instance label of the instance
pulumi.export("instance_label", instance.label)
pulumi.export("instance_ip", instance.ip_address)

