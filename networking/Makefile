PULUMI_DIR ?= test

.PHONY: test
test: infra ansible

.PHONY: infra
infra:
	pulumi -C ${PULUMI_DIR} up --yes

.PHONY: ansible
ansible:
	ansible-playbook -i ./inventory.ini playbooks/k3s.yaml

.PHONY: down
down:
	pulumi -C ${PULUMI_DIR} destroy --yes
