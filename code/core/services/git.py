import os
import subprocess
from tempfile import NamedTemporaryFile

import hvac
from django.conf import settings
from github import Github

from core.contextmanagers import cd
from core.utils.ssh import generate_keys


class GitClient(object):
    def __init__(self, user):
        social = user.social_auth.get(provider='github')
        self._github = Github(social.extra_data['access_token'])
        self._vault_client = None
        self._username = user.username

    @property
    def _vault(self):
        if not self._vault_client:
            self._vault_client = hvac.Client(url='http://localhost:8200', token='just-a-token')
            if 'git/' not in self._vault_client.list_secret_backends():
                self._vault_client.enable_secret_backend('kv', mount_point='git')
        return self._vault_client

    def create_and_save_keys(self, repository):
        private, public = generate_keys()

        self._github.get_user().get_repo(repository).create_key(
            'Airflow As A Service',
            public,
            read_only=True
        )

        self._vault.write(f'git/{self._username}/{repository}', p_key=private)

    def checkout(self, repository, commit_hash):
        private_key = self.get_key(repository)
        env = dict(**os.environ)

        with NamedTemporaryFile() as tf:
            tf.write(private_key.encode())
            tf.seek(0)

            env['GIT_SSH_COMMAND'] = f"ssh -i {tf.name} -F /dev/null"
            self._execute_git_command(f'clone git@github.com:{self._username}/{repository}.git git_checkout/{repository}', env)

            with cd(f'git_checkout/{repository}'):
                self._execute_git_command(f'reset --hard {commit_hash}', env)


    def get_key(self, repository):
        return self._vault.read(f'git/{self._username}/{repository}')['data']['p_key']

    def _execute_git_command(self, cmd, env):
        cmd = [settings.GIT_BINARY, *cmd.split(' ')]

        subprocess.Popen(cmd, env=env).wait()
