PULUMI_DIR ?= infra

.PHONY: up
up: infra ansible

.PHONY: infra
infra:
	export LINDE_TOKEN=$(cat ~/.linode) && \
		pulumi -C ${PULUMI_DIR} up --yes

.PHONY: ansible
ansible:
	ansible-playbook -i ./inventory.ini playbooks/k3s.yaml

.PHONY: down
down:
	pulumi -C ${PULUMI_DIR} destroy --yes
