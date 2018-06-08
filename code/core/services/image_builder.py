import os
from distutils.dir_util import copy_tree
from tempfile import TemporaryDirectory

import docker
from django.conf import settings


class ImageBuilder(object):
    def __init__(self, registry):
        self.client = docker.from_env()
        self.registry = registry

    def build_and_publish(self, tag):
        with TemporaryDirectory() as tmp_dir:
            src = os.path.join(settings.BASE_DIR, 'docker_build')
            copy_tree(src, tmp_dir)

            repo_name = f'{self.registry}/airflow:{tag}'

            self.client.images.build(
                path=tmp_dir,
                tag=repo_name,
                rm=True,
                forcerm=True
            )

            for line in self.client.images.push(repo_name, stream=True):
                print(line.strip())

    def generate_config(self):
        # Build Airflow.cfg file for image with creds for database
        pass
