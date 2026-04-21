# -*- coding: utf-8 -*-

"""
Github repo dataset related
"""

import typing as T
from pathlib import Path

from diskcache import Cache
from github import Github
from sayt2.api import DataSet, NgramField, TextField

from .type_hint import T_RECORD
from .paths import path_enum
from .cache import make_cache
from .config import Config
from .constants import CacheKeyEnum
from .github import download_data, get_repos, get_username

repo_fields = [
    NgramField(name="acc", min_gram=2, max_gram=10, boost=1.0),
    NgramField(name="repo", min_gram=2, max_gram=10, boost=2.0),
    TextField(name="desc"),
]


def make_repo_dataset(
    dir_user: Path,
    downloader: T.Callable[[], list[T_RECORD]],
    cache_expire: int,
) -> DataSet:
    """
    Low-level DataSet constructor. Pure function — no GitHub or config
    dependencies. The caller is responsible for providing the per-user
    directory, a ready-made downloader, and the cache expiry.
    """
    return DataSet(
        dir_root=dir_user,
        name="repo",
        fields=repo_fields,
        downloader=downloader,
        cache_expire=cache_expire,
    )


def make_downloader(
    gh: Github,
    cache: Cache,
    username: str,
    cache_expire: int,
) -> T.Callable[[], list[T_RECORD]]:  # pragma: no cover
    """
    Build the downloader callable used by the repo DataSet.

    Wraps :func:`~afwf_github.github.download_data` with a cache-check:
    if repos are already stored under the per-user cache key, they are
    returned directly without hitting the GitHub API.
    """

    def downloader() -> list[T_RECORD]:
        cache_key = CacheKeyEnum.repos.of(username)
        try:
            repos = get_repos(cache, username) if cache_key in cache else None
        except FileNotFoundError:
            # per-user directory was deleted after cache was opened;
            # fall through to re-download
            repos = None

        if repos is None:
            _, _, repos = download_data(
                gh=gh,
                cache=cache,
                username=username,
                expire=cache_expire,
            )

        seen = set()
        records = []
        for r in repos:
            key = (r["acc"], r["repo"])
            if key not in seen:
                seen.add(key)
                records.append({"acc": r["acc"], "repo": r["repo"], "desc": r["desc"]})
        return records

    return downloader


def create_repo_dataset(config: Config) -> DataSet:  # pragma: no cover
    """
    High-level factory. Derives the GitHub client, username, per-user
    directory, and cache entirely from *config*.
    """
    gh = config.gh
    user = get_username(gh)
    username = user["id"]
    user_dir = path_enum.dir_user(username)
    cache = make_cache(user_dir / ".cache")
    downloader = make_downloader(gh, cache, username, config.cache_expire)
    return make_repo_dataset(user_dir, downloader, config.cache_expire)
