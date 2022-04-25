# -*- coding: utf-8 -*-

"""
GitHub data related.
"""

import json
from typing import List, Dict

from github import Github
from diskcache import Cache

from .paths import path_default_token
from .cache import cache, DEFAULT_EXPIRE


class CacheKeys:
    user = "user"
    accounts = "accounts"
    repos = "repos"


def create_gh_client():
    return Github(path_default_token.read_text().strip())


def refresh_cache(cache: Cache = cache):
    if not path_default_token.exists():
        raise FileNotFoundError

    gh = create_gh_client()

    user = gh.get_user()
    user_id = user.html_url.split("/")[-1]
    user_name = user.name

    accounts = [dict(id=user_id, name=user_name)]
    for org in user.get_orgs():
        account_id = org.html_url.split("/")[-1]
        account_name = org.name
        accounts.append(dict(id=account_id, name=account_name))

    repos = list()
    for repo in user.get_repos():
        account_name = repo.full_name.split("/")[0]
        repo_name = repo.name
        repo_description = repo.description
        repos.append(dict(acc=account_name, repo=repo_name, desc=repo_description))

    cache.set(CacheKeys.user, json.dumps(dict(id=user_id, name=user_name)), expire=DEFAULT_EXPIRE)
    cache.set(CacheKeys.accounts, json.dumps(accounts), expire=DEFAULT_EXPIRE)
    cache.set(CacheKeys.repos, json.dumps(repos), expire=DEFAULT_EXPIRE)


def get_user(cache: Cache = cache) -> Dict[str, str]:
    return json.loads(cache.get(CacheKeys.user))


def get_accounts(cache: Cache = cache) -> List[Dict[str, str]]:
    return json.loads(cache.get(CacheKeys.accounts))


def get_repos(cache: Cache = cache) -> List[Dict[str, str]]:
    return json.loads(cache.get(CacheKeys.repos))
