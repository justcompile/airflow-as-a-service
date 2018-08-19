import unittest
from unittest import mock

from django.contrib.auth import get_user_model

from scm.tasks import setup_repository


class SetupRepositoryTestCase(unittest.TestCase):
    def setUp(self):
        client_patch = mock.patch('scm.tasks.get_client_for_dvcs')
        self.client = client_patch.start().return_value
        self.addCleanup(client_patch.stop)

        self.user = get_user_model().objects.create_user('testuser')

    def tearDown(self):
        get_user_model().objects.all().delete()

    def test_does_not_do_anything_more_if_repo_has_key_defined(self):
        self.client().repo_has_ssh_key.return_value = True

        setup_repository(self.user.id, 'my-repo')

        self.client().create_and_save_keys.assert_not_called()

    def test_creates_keys_and_registers_webhook_if_key_doesnt_exist(self):
        self.client().repo_has_ssh_key.return_value = False

        setup_repository(self.user.id, 'my-repo')

        self.client().create_and_save_keys.assert_called_with('my-repo')
        self.client().register_webhook.assert_called_with('my-repo')
