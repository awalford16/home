PULUMI_DIR ?= deploy
LINODE_TOKEN=$$(cat ~/.linode)
GITHUB_TOKEN=$$(cat ~/.github)
stack ?= lab
workers ?= 0

.PHONY: up
up: nodes wait_for_ready ansible bootstrap

.PHONY: nodes
nodes:
	export LINODE_TOKEN=${LINODE_TOKEN} && \
		pulumi up -C $@ --stack ${stack} -c worker_nodes=${workers} --yes

.PHONY: wait_for_ready
wait_for_ready:
	@$$(sleep 10)

.PHONY: ansible
ansible:
	ansible-playbook -i ./inventory.ini playbooks/k3s.yaml --extra-vars="stack=${stack}"

.PHONY: ansible-cilium
ansible-cilium:
	ansible-playbook -i ./inventory.ini playbooks/k3s.yaml --extra-vars="stack=${stack}" -t cilium


.PHONY: ansible-system
ansible-system:
	ansible-playbook -i ./inventory.ini playbooks/k3s.yaml --extra-vars="stack=${stack}" -t system


.PHONY: bootstrap
bootstrap:
	export GITHUB_TOKEN=${GITHUB_TOKEN} && export KUBECONFIG="~/.kube/${stack}" && \
		pulumi -C $@ up --stack ${stack} --yes

.PHONY: down
down:
	pulumi destroy --stack ${stack} --yes
