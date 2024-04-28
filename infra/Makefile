PULUMI_DIR ?= deploy
LINODE_TOKEN=$$(cat ~/.linode)
stack ?= lab

.PHONY: up
up: infra ansible

.PHONY: infra
infra:
	export LINODE_TOKEN=${LINODE_TOKEN} && \
		pulumi up --stack ${stack} --yes

.PHONY: ansible
ansible:
	ansible-playbook -i ./inventory.ini playbooks/k3s.yaml --extra-vars="stack=${stack}"

.PHONY: down
down:
	pulumi -C ${PULUMI_DIR} destroy --stack ${stack} --yes