from contextlib import contextmanager
from django.conf import settings
from jinja2 import Environment, FileSystemLoader


env = Environment(
    loader=FileSystemLoader(settings.K8S['TEMPLATE_DIR'])
)

@contextmanager
def compile_template(file_path, **params):
    template = env.get_template(file_path)
    yield template.render(**params)
