class GitHubFormatter(object):
    @classmethod
    def parse_commit(cls, commit, repo, branch="master"):
        return {
            "committer": commit.committer.login,
            "commit_id": commit.sha,
            "repo_url": repo.url,
            "branch": branch,
        }

    @classmethod
    def parse_webhook_message(cls, commit):
        return {
            "committer": commit["head_commit"]["author"]["username"],
            "commit_id": commit["head_commit"]["id"],
            "repo_url": commit["repository"]["html_url"],
            "branch": commit["ref"],
            "message": commit["head_commit"]["message"],
        }
