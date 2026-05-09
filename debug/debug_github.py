# -*- coding: utf-8 -*-

from afwf_github.github import download_data
from afwf_github.github import get_username
from afwf_github.github import get_user
from afwf_github.github import get_accounts
from afwf_github.github import get_repos
from afwf_github.paths import path_enum
from afwf_github.config import Config
from afwf_github.cache import make_cache
from rich import print as rprint

# page_limit = 3
page_limit = 9999

config = Config.load(path_enum.path_config_json)
gh = config.gh
user = get_username(gh)
username = user["id"]
user_dir = path_enum.dir_user(username)
cache = make_cache(user_dir / ".cache")

def _download_data():
    download_data(
        gh=gh,
        cache=cache,
        username=username,
        expire=30 * 24 * 3600,
        page_limit=page_limit,
        verbose=True,
    )

_download_data()

user = get_user(cache=cache, username=username)
# rprint(user)

accounts = get_accounts(cache=cache, username=username)
# rprint(accounts[:10])

repos = get_repos(cache=cache, username=username)
# rprint(repos[:10])
print(f"n repo = {len(repos)}")

for repo in repos:
    print(repo)
