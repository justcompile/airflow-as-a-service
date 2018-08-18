import unittest
from unittest import mock

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

    # FIXME: TESTS HERE
    def test_repo_has_key_returns_false_if_keyname_not_in_github_keys(self):
        self.git().get_user().get_repo().get_keys.return_value = []

        client = GitClient(self.mock_user)

        self.assertFalse(client.repo_has_ssh_key('my-repo'))

    def test_repo_has_key_returns_true_if_keyname_is_in_github_keys(self):
        self.git().get_user().get_repo().get_keys.return_value = [
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
