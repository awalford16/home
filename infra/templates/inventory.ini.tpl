[k3s-master]
{{ ip_address }} ansible_ssh_user={{ user or "root" }}

[k3s-workers]
{% for worker in workers %}
{{ worker }}
{% endfor %}

[k3s-workers:vars]
master_node_url=https://{{ ip_address }}:6443
