# -*- coding: utf-8 -*-

"""
GitHub data related.
"""

import typing as T
import json
import itertools

from github import Github, GithubException
from diskcache import Cache

from .constants import CacheKeyEnum


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


def get_username(gh: Github) -> UserType:
    """Return the id and display name for the authenticated GitHub user.

    This is a single lightweight API call used to determine the per-user
    data directory before any heavier operations run.
    ``id`` is the GitHub login (used for directory names and cache keys);
    ``name`` is the human-readable display name.
    """
    try:
        gh_user = gh.get_user()
        user_id: str = gh_user.html_url.split("/")[-1]
        user_name: str = gh_user.name or user_id
        return UserType(id=user_id, name=user_name)
    except GithubException as e:
        raise RuntimeError(
            f"Failed to get GitHub username (status={e.status}): {e.data}"
        ) from e
    except Exception as e:
        raise RuntimeError(f"Unexpected error getting GitHub username: {e}") from e


def take(iterable: T.Iterable, n: int) -> list:
    """
    Return first n items of the iterable as a list.

    Example::

        >>> take([0, 1, 2], 2)
        [0, 1]
    """
    return list(itertools.islice(iterable, n))


def fetch_data(
    gh: Github,
    page_limit: int = 9999,
    verbose: bool = False,
) -> tuple[
    UserType,
    list[AccountType],
    list[RepoType],
]:
    """
    Pull user, accounts, and repos from the GitHub API. No caching.
    Each API call is treated as potentially failing and raises a descriptive
    RuntimeError on unexpected errors. 403 responses on individual orgs or
    repos are silently skipped — the user simply lacks permission for those.
    """
    try:
        gh_user = gh.get_user()
        user_id: str = gh_user.html_url.split("/")[-1]
        user_name: str = gh_user.name or user_id
    except GithubException as e:
        raise RuntimeError(
            f"Failed to fetch authenticated user from GitHub (status={e.status}): {e.data}"
        ) from e
    except Exception as e:
        raise RuntimeError(f"Unexpected error fetching authenticated user: {e}") from e

    if verbose:
        print(f"Fetched user: {user_name} ({user_id})")

    accounts: list[AccountType] = [AccountType(id=user_id, name=user_name)]
    for org in take(gh_user.get_orgs(), page_limit):
        try:
            account_id: str = org.html_url.split("/")[-1]
            account_name: str = org.name or account_id
            if verbose:
                print(f"Fetched org: {account_name} ({account_id})")
            accounts.append(AccountType(id=account_id, name=account_name))
        except GithubException as e:
            if e.status == 403:
                if verbose:
                    print(f"Skipped org (no permission, status=403): {e.data}")
            else:
                raise RuntimeError(
                    f"Failed to fetch org details (status={e.status}): {e.data}"
                ) from e
        except Exception as e:
            raise RuntimeError(f"Unexpected error fetching org: {e}") from e

    repos: list[RepoType] = []
    for repo in take(gh_user.get_repos(visibility="all"), page_limit):
        try:
            account_name = repo.full_name.split("/")[0]
            repo_name: str = repo.name
            repo_desc: str = repo.description or ""
            if verbose:
                print(f"Fetched repo: {account_name}/{repo_name}")
            repos.append(RepoType(acc=account_name, repo=repo_name, desc=repo_desc))
        except GithubException as e:
            if e.status == 403:
                if verbose:
                    print(f"Skipped repo (no permission, status=403): {e.data}")
            else:
                raise RuntimeError(
                    f"Failed to fetch repo details (status={e.status}): {e.data}"
                ) from e
        except Exception as e:
            raise RuntimeError(f"Unexpected error fetching repo: {e}") from e

    user: UserType = UserType(id=user_id, name=user_name)
    return user, accounts, repos


def download_data(
    gh: Github,
    cache: Cache,
    username: str,
    expire: int,
    page_limit: int = 9999,
    verbose: bool = False,
) -> tuple[
    UserType,
    list[AccountType],
    list[RepoType],
]:
    """
    Pull data from GitHub via :func:`fetch_data` and store results in cache
    under per-username keys (e.g. ``repos@alice``).
    """
    user, accounts, repos = fetch_data(gh, page_limit=page_limit, verbose=verbose)
    cache.set(CacheKeyEnum.user.of(username), json.dumps(user), expire=expire)
    cache.set(CacheKeyEnum.accounts.of(username), json.dumps(accounts), expire=expire)
    cache.set(CacheKeyEnum.repos.of(username), json.dumps(repos), expire=expire)
    return user, accounts, repos


def get_user(
    cache: Cache,
    username: str,
) -> UserType:
    return json.loads(cache.get(CacheKeyEnum.user.of(username)))


def get_accounts(
    cache: Cache,
    username: str,
) -> list[AccountType]:
    return json.loads(cache.get(CacheKeyEnum.accounts.of(username)))


def get_repos(
    cache: Cache,
    username: str,
) -> list[RepoType]:
    return json.loads(cache.get(CacheKeyEnum.repos.of(username)))
