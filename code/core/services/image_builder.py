import json
import os
from base64 import b64decode
from distutils.dir_util import copy_tree

import docker
from django.conf import settings
from jinja2 import Template


class ImageBuilder(object):
    def __init__(self, registry):
        self.client = docker.from_env()
        self.registry = registry

    def build_and_publish(self, build_dir, cluster, secret, tag=None):
        tag = tag or cluster.id

        docker_files_dir = os.path.join(settings.BASE_DIR, 'docker_build')
        copy_tree(docker_files_dir, build_dir)

        db_connection = self._secret_to_db_connection(secret)

        self.generate_config(build_dir, cluster_id=cluster.id, **db_connection)

        repo_name = f'{self.registry}/airflow:{tag}'

        for line in self.client.api.build(path=build_dir, tag=repo_name, rm=True, forcerm=True):
            self._parse_message(line, 'stream')

        for line in self.client.images.push(repo_name, stream=True):
            self._parse_message(line, 'status')

        return repo_name.replace(self.registry, '')

    def generate_config(self, dir_name, **data):
        # Build Airflow.cfg file for image with creds for database

        with open(os.path.join(dir_name, 'airflow.cfg')) as reader:
            config = reader.read()

        # do some rendering stuffs
        with open(os.path.join(dir_name, 'airflow.cfg'), 'w+') as writer:
            new_config = Template(config).render(**data)
            writer.write(new_config)

    def _secret_to_db_connection(self, secret):
        # attempt to extract db protocol from secret keys
        key_prefixes = [k.split('-')[0] for k in secret.data.keys()]
        if set(key_prefixes) == {key_prefixes[0]}:
            protocol = key_prefixes[0]
        else:
            raise ValueError('Unable to determine DB protocol')

        context = {
            k.split('-')[-1]: b64decode(v).decode()
            for k, v in secret.data.items()
        }
        context['protocol'] = protocol

        return context

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
