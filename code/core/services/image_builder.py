import json
import logging
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

            for line in self.client.api.build(path=tmp_dir, tag=repo_name, rm=True, forcerm=True):
                self._parse_message(line, 'stream')

            for line in self.client.images.push(repo_name, stream=True):
                self._parse_message(line, 'status')

    def generate_config(self):
        # Build Airflow.cfg file for image with creds for database
        pass

    def _parse_message(self, message, key):
        for line in message.strip().split(b'\r\n'):
            try:
                text = json.loads(line)[key]
                if text != '\n':
                    print(text)
            except json.JSONDecodeError:
                print('ERROR: %s' % message)
            except KeyError:
                print(json.loads(line))
