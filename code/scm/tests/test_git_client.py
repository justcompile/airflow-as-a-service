import ast
import inspect
import unittest
from unittest import mock

from django.apps import apps
from django.contrib.auth.models import User
from django.db.models.signals import ModelSignal
from core import signals
from core.models import Build, Repository
from scm.git import GitClient, SSH_KEY_NAME


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        git_patch = mock.patch('scm.git.Github')
        self.git = git_patch.start()
        self.addCleanup(git_patch.stop)

        hvac_patch = mock.patch('scm.git.hvac.Client')
        self.hvac = hvac_patch.start()
        self.addCleanup(hvac_patch.stop)

        self.user_data = {
            'access_token': 'foobar',
        }

        self.mock_user = mock.Mock(username='testuser')
        self.mock_user.social_auth.get.side_effect = lambda **_: mock.Mock(
            extra_data=self.user_data,
        )

        settings_patch = mock.patch('scm.git.settings')
        self.settings = settings_patch.start()
        self.addCleanup(settings_patch.stop)

        generate_keys_patch = mock.patch('scm.git.generate_keys')
        self.generate_keys = generate_keys_patch.start()
        self.addCleanup(generate_keys_patch.stop)

    def tearDown(self):
        User.objects.all().delete()


class GitClientTestCase(BaseTestCase):
    def test_init_creates_github_instances_with_users_access_token(self):
        GitClient(self.mock_user)
        self.git.assert_called_with('foobar')

    def test_vault_is_not_lazy_loaded_if_set(self):
        client = GitClient(self.mock_user)
        client._vault_client = {}
        client._vault

        self.hvac.assert_not_called()

    def test_vault_is_lazy_loaded_if_not_set(self):
        self.settings.VAULT = {
            'token': 'my-token',
            'url': 'http://consul:8200',
        }

        client = GitClient(self.mock_user)
        client._vault

        self.hvac.assert_called_with(
            token='my-token',
            url='http://consul:8200',
        )

    def test_vault_does_not_create_backend_if_already_exists(self):
        self.settings.VAULT = {
            'token': 'my-token',
            'url': 'http://consul:8200',
        }

        self.hvac().list_secret_backends.return_value = ['git/']

        client = GitClient(self.mock_user)
        client._vault

        self.hvac().enable_secret_backend.assert_not_called()

    def test_vault_does_create_backend_if_does_not_exists(self):
        self.settings.VAULT = {
            'token': 'my-token',
            'url': 'http://consul:8200',
        }

        self.hvac().list_secret_backends.return_value = []

        client = GitClient(self.mock_user)
        client._vault

        self.hvac().enable_secret_backend.assert_called_with('kv', mount_point='git')


class GitClientMethodsTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()

        self.settings.VAULT = {
            'token': 'my-token',
            'url': 'http://consul:8200',
        }

        subprocess_patch = mock.patch('scm.git.subprocess')
        self.subprocess = subprocess_patch.start()
        self.addCleanup(subprocess_patch.stop)

    def test_create_and_save_keys_sends_public_key_to_github(self):
        self.generate_keys.return_value = ('private-key', 'public-key')
        client = GitClient(self.mock_user)

        client.create_and_save_keys('my-repo')

        self.git().get_user().get_repo().create_key.assert_called_with(
            SSH_KEY_NAME,
            'public-key',
            read_only=True,
        )

    def test_create_and_save_keys_sends_private_key_to_consul(self):
        self.generate_keys.return_value = ('private-key', 'public-key')
        client = GitClient(self.mock_user)

        client.create_and_save_keys('my-repo')

        self.hvac().write.assert_called_with(
            f'git/{self.mock_user.username}/my-repo',
            p_key='private-key',
        )

    @mock.patch('scm.git.NamedTemporaryFile')
    @mock.patch('scm.git.cd')
    def test_checkout_retrieves_private_key_from_consul_and_writes_to_tmp_file(self, mock_cd, mock_tmp_file):
        client = GitClient(self.mock_user)
        client._vault_client = mock.Mock()
        client._vault_client.read.return_value = {
            'data': {
                'p_key': 'private',
            },
        }

        client.checkout('my-repo', '12345', 'some_dir')
        self.assertEqual(client._vault_client.read.call_count, 1)
        mock_tmp_file().__enter__().write.assert_called_with(b'private')

    @mock.patch('scm.git.NamedTemporaryFile')
    @mock.patch('scm.git.cd')
    @mock.patch('scm.git.os')
    def test_checkout_clones_git_repo(self, mock_os, mock_cd, mock_tmp_file):
        mock_os.environ = {}

        self.settings.GIT_BINARY = 'git'

        client = GitClient(self.mock_user)
        client._vault_client = mock.Mock()
        client._vault_client.read.return_value = {
            'data': {
                'p_key': 'private',
            },
        }

        mock_tmp_file().__enter__().name = 'my-tmp-file'

        client.checkout('my-repo', '12345', 'some_dir')
        self.subprocess.Popen.assert_has_calls([
            mock.call(
                'git clone git@github.com:testuser/my-repo.git some_dir/my-repo'.split(),
                env={
                    'GIT_SSH_COMMAND': 'ssh -i my-tmp-file -F /dev/null',
                },
            ),
            mock.call().wait(),
            mock.call(
                'git reset --hard 12345'.split(),
                env={
                    'GIT_SSH_COMMAND': 'ssh -i my-tmp-file -F /dev/null',
                },
            )],
            mock.call().wait(),
        )

    def test_repo_has_key_returns_false_if_keyname_not_in_github_keys(self):
        self.git().get_user().get_repo().get_keys.return_value = []

        client = GitClient(self.mock_user)

        self.assertFalse(client.repo_has_ssh_key('my-repo'))

    def test_repo_has_key_returns_true_if_keyname_is_in_github_keys(self):
        self.git().get_user().get_repo().get_keys.return_value = [
            mock.Mock(title='meh'),
            mock.Mock(title=SSH_KEY_NAME),
        ]

        client = GitClient(self.mock_user)

        self.assertTrue(client.repo_has_ssh_key('my-repo'))

    def test_get_key_calls_vault_with_correct_path(self):
        client = GitClient(self.mock_user)
        client._vault_client = mock.Mock()
        client._vault_client.read.return_value = {
            'data': {
                'p_key': 'private',
            },
        }

        client.get_key('my-repo')

        client._vault_client.read.assert_called_with(f'git/{self.mock_user.username}/my-repo')

    def test_get_key_returns_none_if_not_found(self):
        client = GitClient(self.mock_user)
        client._vault_client = mock.Mock()
        client._vault_client.read.return_value = {}

        self.assertIsNone(client.get_key('my-repo'))

    def test_register_webhook_calls_github_with_correct_parameters(self):
        self.settings.GITHUB_PUSH_EVENT_WEBHOOK_URL = 'push-me'
        self.settings.DEBUG = True

        client = GitClient(self.mock_user)
        client.register_webhook('my-repo')

        self.git().get_user().get_repo().create_hook.assert_called_with(
            "web",
            dict(
                url='push-me',
                content_type="json",
                insecure_ssl='1',
            ),
            events=["push"],
            active=True,
        )

    def test_create_build_for_latest_commit_returns_build_instance(self):
        self._disconnect_signals()

        commit = mock.Mock(sha='sha-123')
        commit.committer.login = 'username'

        self.git().get_user().get_repo().get_commits.return_value = [
            commit,
        ]

        repo = Repository.objects.create(
            owner=User.objects.create_user('myuser'),
            url='http://myurl.com/my-repo',
        )
        client = GitClient(self.mock_user)

        result = client.create_build_for_latest_commit(repo)
        self.assertIsInstance(result, Build)

    def _disconnect_signals(self):
        signal_attrs = [
            x
            for x in inspect.getmembers(signals)
            if not x[0].startswith('__')
        ]

        django_signals = dict(
            (name, func)
            for name, func in signal_attrs
            if isinstance(func, ModelSignal)
        )

        module_signals = [
            signal
            for _, signal in signal_attrs
            if signal.__module__ == signals.__name__
        ]

        for signal_func in module_signals:
            module = ast.parse(inspect.getsource(signal_func))
            for decorator in module.body[0].decorator_list:
                if decorator.func.id == 'receiver':
                    django_signals[decorator.args[0].id].disconnect(
                        signal_func,
                        sender=apps.get_model(
                            app_label=signals.__name__.split('.')[0],
                            model_name=decorator.keywords[0].value.id,
                        ),
                    )
