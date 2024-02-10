.PHONY: test
test:
	pulumi -C test up --yes && \
	ansible-playbook -i ./inventory.ini playbooks/k3s.yaml --check
# Run some ansible

