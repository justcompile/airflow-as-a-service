import os
import subprocess
from tempfile import NamedTemporaryFile

import hvac
from django.conf import settings
from github import Github

from core.contextmanagers import cd
from core.models import Build
from core.utils.ssh import generate_keys
from .commit_formatters import GitHubFormatter


class GitClient(object):
    Formatter = GitHubFormatter

    def __init__(self, user):
        social = user.social_auth.get(provider='github')
        self._github = Github(social.extra_data['access_token'])
        self._vault_client = None
        self._username = user.username

    @property
    def _vault(self):
        if not self._vault_client:
            self._vault_client = hvac.Client(**settings.VAULT)
            if 'git/' not in self._vault_client.list_secret_backends():
                self._vault_client.enable_secret_backend('kv', mount_point='git')
        return self._vault_client

    def create_and_save_keys(self, repository):
        private, public = generate_keys()

        self._get_repo(repository).create_key(
            'Airflow As A Service',
            public,
            read_only=True
        )

        self._vault.write(f'git/{self._username}/{repository}', p_key=private)

    def checkout(self, repository, commit_hash, clone_dir):
        private_key = self.get_key(repository)
        env = dict(**os.environ)

        with NamedTemporaryFile() as tf:
            tf.write(private_key.encode())
            tf.seek(0)

            env['GIT_SSH_COMMAND'] = f"ssh -i {tf.name} -F /dev/null"
            self._execute_git_command(f'clone git@github.com:{self._username}/{repository}.git {clone_dir}/{repository}', env)

            with cd(f'{clone_dir}/{repository}'):
                self._execute_git_command(f'reset --hard {commit_hash}', env)

    def create_build_for_latest_commit(self, repository):
        latest_commit = self._get_repo(repository.name).get_commits(sha='master')[0]

        parsed_commit = self.Formatter.parse_commit(latest_commit, repository)

        return Build.objects.create(
            committer=parsed_commit["committer"],
            commit_id=parsed_commit["commit_id"],
            branch=parsed_commit["branch"],
            status=Build.QUEUED,
            repository=repository
        )

    def get_key(self, repository):
        return self._vault.read(f'git/{self._username}/{repository}')['data']['p_key']

    def register_webhook(self, repository):
        self._get_repo(repository).create_hook(
            "web",
            dict(
                url=settings.GITHUB_PUSH_EVENT_WEBHOOK_URL,
                content_type="json",
                insecure_ssl='1' if settings.DEBUG else '0',
            ),
            events=["push"],
            active=True,
        )

    def _get_repo(self, name):
        return self._github.get_user().get_repo(name)

    def _execute_git_command(self, cmd, env):
        cmd = [settings.GIT_BINARY, *cmd.split(' ')]

        subprocess.Popen(cmd, env=env).wait()
