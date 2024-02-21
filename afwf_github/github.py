# -*- coding: utf-8 -*-

"""
GitHub data related.
"""

import typing as T
import json
import itertools

from github import Github, GithubException
from diskcache import Cache

from .cache import cache
from .config import config


class CacheKeyEnum:
    user = "user"
    accounts = "accounts"
    repos = "repos"


def create_gh_client():
    """
    Create github client with default token.
    """
    return Github(config.pac_token)


def take(iterable: T.Iterable, n: int) -> T.Iterable:
    """
    Return first n items of the iterable as a list.

    Example::

        >>> take([0, 1, 2], 2)
        [0, 1]

    **中文文档**

    取出可循环对象中的前 n 个元素. 等效于 ``list(iterable)[:n]``, 但占用极小的内存.
    因为 ``list(iterable)`` 要将所有元素放在内存中并生成一个新列表. 该方法常用于
    那些无法做取 index 操作的可循环对象.
    """
    return list(itertools.islice(iterable, n))


class UserType(T.TypedDict):
    id: str
    name: str


class AccountType(T.TypedDict):
    id: str
    name: str


class RepoType(T.TypedDict):
    acc: str
    repo: str
    desc: str


def download_data(
    gh: Github,
    cache: Cache = cache,
    page_limit: int = 9999,
    verbose: bool = False,
) -> T.Tuple[UserType, T.List[AccountType], T.List[RepoType]]:
    user = gh.get_user()
    user_id = user.html_url.split("/")[-1]
    user_name = user.name

    if verbose:
        print(f"user_name: {user_name}")

    accounts = [dict(id=user_id, name=user_name)]
    for org in take(user.get_orgs(), page_limit):
        try:
            account_id = org.html_url.split("/")[-1]
            account_name = org.name
            if verbose:
                print(f"account_name: {account_name}")
            accounts.append(dict(id=account_id, name=account_name))
        except GithubException as e:  # pragma: no cover
            if e.status == 403:
                pass
            else:
                raise e
        except Exception as e:  # pragma: no cover
            raise e

    repos = list()
    for repo in take(user.get_repos(visibility="all"), page_limit):
        try:
            account_name = repo.full_name.split("/")[0]
            repo_name = repo.name
            if verbose:
                print(f"repo_name: {account_name}/{repo_name}")
            repo_description = repo.description
            repos.append(dict(acc=account_name, repo=repo_name, desc=repo_description))
        except GithubException as e:  # pragma: no cover
            if e.status == 403:
                pass
            else:
                raise e
        except Exception as e:  # pragma: no cover
            raise e

    user = dict(id=user_id, name=user_name)
    cache.set(
        CacheKeyEnum.user,
        json.dumps(dict(id=user_id, name=user_name)),
        expire=3600,
    )
    cache.set(
        CacheKeyEnum.accounts,
        json.dumps(accounts),
        expire=3600,
    )
    cache.set(
        CacheKeyEnum.repos,
        json.dumps(repos),
        expire=3600,
    )

    return user, accounts, repos


def get_user(cache: Cache = cache) -> UserType:
    return json.loads(cache.get(CacheKeyEnum.user))


def get_accounts(cache: Cache = cache) -> T.List[AccountType]:
    return json.loads(cache.get(CacheKeyEnum.accounts))


def get_repos(cache: Cache = cache) -> T.List[RepoType]:
    return json.loads(cache.get(CacheKeyEnum.repos))
