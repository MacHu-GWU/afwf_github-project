# -*- coding: utf-8 -*-

import typing as T

from diskcache import Cache
from github import Github
from sayt2.api import DataSet, NgramField, TextField

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


def create_repo_dataset(
    config: Config,
    cache: Cache | None = None,
    _downloader: T.Callable[[], list[dict]] | None = None,
) -> DataSet:
    """
    Create the repo search DataSet.

    The GitHub client and username are derived from *config* internally.
    All data — GitHub API responses (diskcache) and the sayt2 search index —
    is stored under ``path_enum.dir_user(username)``. Deleting that directory
    resets everything for that user.

    :param config: App config — provides the PAC token (used to build the
        GitHub client and resolve the username) and cache expiry.
    :param cache: diskcache instance for GitHub API responses. Defaults to a
        cache at ``{dir_user}/.cache/``. Mainly overridden in tests.
    :param _downloader: Override the default downloader. Intended for testing
        only — allows injecting a fake data source without hitting GitHub.
    """
    gh = Github(config.pac_token)
    user = get_username(gh)
    username = user["id"]
    user_dir = path_enum.dir_user(username)

    if cache is None:
        cache = make_cache(user_dir / ".cache")

    def _default_downloader() -> list[dict]:
        cache_key = CacheKeyEnum.repos.of(username)
        try:
            repos = get_repos(cache, username) if cache_key in cache else None
        except FileNotFoundError:
            # per-user directory was deleted between cache creation and access;
            # diskcache will recreate it on the next make_cache call
            repos = None

        if repos is None:
            _, _, repos = download_data(
                gh, cache, username, expire=config.cache_expire
            )

        return [
            {"acc": r["acc"], "repo": r["repo"], "desc": r["desc"]}
            for r in repos
        ]

    return DataSet(
        dir_root=user_dir,
        name="repo",
        fields=repo_fields,
        downloader=_downloader or _default_downloader,
        cache_expire=config.cache_expire,
    )
