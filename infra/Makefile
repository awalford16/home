PULUMI_DIR ?= deploy
LINODE_TOKEN=$$(cat ~/.linode)
stack ?= lab
workers ?= 0

.PHONY: up
up: infra ansible

.PHONY: infra
infra:
	export LINODE_TOKEN=${LINODE_TOKEN} && \
		pulumi up --stack ${stack} -c worker_nodes=${workers} --yes

.PHONY: ansible
ansible:
	ansible-playbook -i ./inventory.ini playbooks/k3s.yaml --extra-vars="stack=${stack}"

.PHONY: down
down:
	pulumi destroy --stack ${stack} --yes
