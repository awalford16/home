from jinja2 import Environment, FileSystemLoader
import os

TEMPLATE_FILES = os.path.dirname(__file__) + "/templates"


def get_file_path(file):
    normalised_path = os.path.normpath(file)
    return os.path.dirname(normalised_path)

def create_inventory(template_file, destination, **kwargs):
    environment = Environment(loader=FileSystemLoader(TEMPLATE_FILES))
    template = environment.get_template(template_file)
   
    kwargs_string = ', '.join(['{}={}'.format(key, value) for key, value in kwargs.items()])
    print(kwargs_string)
    os.makedirs(get_file_path(destination), exist_ok=True)
    content = template.render(**kwargs)
    with open(destination, mode="w", encoding="utf-8") as message:
        message.write(content)
