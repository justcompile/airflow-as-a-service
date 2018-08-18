import unittest
from unittest import mock

from scm.commit_formatters import GitHubFormatter


class GithubFormatterTestCase(unittest.TestCase):
    def test_parse_commit_uses_default_branch_name_if_not_supplied(self):
        expected_result = {
            'committer': 'username',
            'commit_id': 'sha-123',
            'repo_url': 'http://myurl.com/my-repo',
            'branch': 'master',
        }

        commit = mock.Mock(sha='sha-123')
        commit.committer.login = 'username'
        repo = mock.Mock(url='http://myurl.com/my-repo')

        actual_result = GitHubFormatter.parse_commit(commit, repo)
        self.assertEqual(expected_result, actual_result)

    def test_parse_commit_returns_dict_with_supplied_branch_name(self):
        expected_result = {
            'committer': 'username',
            'commit_id': 'sha-123',
            'repo_url': 'http://myurl.com/my-repo',
            'branch': 'feature/omg-123',
        }

        commit = mock.Mock(sha='sha-123')
        commit.committer.login = 'username'
        repo = mock.Mock(url='http://myurl.com/my-repo')

        actual_result = GitHubFormatter.parse_commit(commit, repo, 'feature/omg-123')
        self.assertEqual(expected_result, actual_result)

    def test_parse_webhook_message_returns_dict(self):
        expected_result = {
            "committer": 'my-username',
            "commit_id": 'id-123',
            "repo_url": 'http://myurl.com/my-repo',
            "branch": 'branch-123',
            "message": 'did a thing',
        }

        commit = {
            'head_commit': {
                'author': {
                    'username': 'my-username',
                },
                'id': 'id-123',
                'message': 'did a thing',
            },
            'repository': {
                'html_url': 'http://myurl.com/my-repo',
            },
            'ref': 'branch-123',
        }

        actual_result = GitHubFormatter.parse_webhook_message(commit)
        self.assertEqual(expected_result, actual_result)
