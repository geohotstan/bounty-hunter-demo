from typing import Optional
from github import Github

github = Github()
class GitWrapper_:
    def __init__(self, repo: Optional[str] = None):
        self.repo = github.get_repo("tinygrad/tinygrad" if repo is not None else repo)
        self.bounties = [issue for issue in repo.get_issues(labels=["bounty"])]
