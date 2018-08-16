import os
from contextlib import contextmanager

from django.conf import settings
from jinja2 import Environment, FileSystemLoader


env = Environment(
    loader=FileSystemLoader(settings.K8S['TEMPLATE_DIR']),
)


@contextmanager
def compile_template(file_path, **params):
    template = env.get_template(file_path)
    yield template.render(**params)


@contextmanager
def cd(path):
    """
    A context manager which changes the working directory to the given
    path, and then changes it back to its previous value on exit.
    Usage:
    > # Do something in original directory
    > with cd('/my/new/path'):
    >     # Do something in new directory
    > # Back to old directory
    """

    prev_cwd = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(prev_cwd)
