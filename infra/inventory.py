from jinja2 import Environment, FileSystemLoader
import os

TEMPLATE_FILES = os.path.dirname(__file__) + "/templates"


def create_inventory(ip_address, template_file, destination):
    environment = Environment(loader=FileSystemLoader(TEMPLATE_FILES))
    template = environment.get_template(template_file)

    content = template.render(ip_address=ip_address)
    with open(destination, mode="w", encoding="utf-8") as message:
        message.write(content)
