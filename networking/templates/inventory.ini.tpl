[k3s-master]
{{ ip_address }} ansible_ssh_user={{ user or "root" }}

[k3s-nodes]
{% for item in slaves %}
{{ item }}
{% endfor %}