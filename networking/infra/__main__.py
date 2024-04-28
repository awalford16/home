"""A Linode Python Pulumi program"""

import pulumi
import pulumi_linode
import inventory
import os
from pathlib import Path

SSH_FILE_PATH = os.environ.get("SSH_FILE_PATH", f"{str(Path.home())}/.ssh/id_ed25519.pub")

ssh_file = open(SSH_FILE_PATH, "r")
stack_name = pulumi.get_stack()

# Create a Linode resource (Linode Instance)
instance = pulumi_linode.Instance(
    f"k3s-{stack_name}-master",
    authorized_keys=[ssh_file.readline().replace("\n", "")],
    type="g6-nanode-1",
    region="eu-west",
    label=f"{stack_name}",
    image="linode/ubuntu22.04",
)

# Write to inventory file
inventory_file = os.path.dirname(__file__) + "/../inventory.ini"
var_file = os.path.dirname(__file__) + "/../group_vars/k3s-nodes.yaml"
instance.ip_address.apply(
    lambda ip: inventory.create_inventory(
        ip_address=ip, template_file="inventory.ini.tpl", destination=inventory_file
    )
)

# Export the Instance label of the instance
pulumi.export("instance_label", instance.label)
pulumi.export("instance_ip", instance.ip_address)
