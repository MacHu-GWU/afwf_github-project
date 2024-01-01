# -*- coding: utf-8 -*-

import sayt.api as sayt

from .paths import dir_repo_index
from .cache import cache, search_cache
from .github import CacheKeyEnum, create_gh_client, download_data, get_repos


repo_fields = [
    sayt.TextField(name="acc", stored=True),
    sayt.TextField(name="repo", stored=True),
    sayt.NgramWordsField(
        name="acc_ngram",
        stored=True,
        minsize=2,
        maxsize=10,
    ),
    sayt.NgramWordsField(
        name="repo_ngram",
        stored=True,
        minsize=2,
        maxsize=10,
    ),
    sayt.StoredField(name="desc"),
]


def download_repos():
    if CacheKeyEnum.repos in cache:
        return get_repos(cache)
    else:
        gh = create_gh_client()
        _, _, repos = download_data(gh, cache)
        return repos


def downloader():
    repos = download_repos()
    for repo in repos:
        print(repo)
        yield {
            "acc": repo["acc"],
            "repo": repo["repo"],
            "acc_ngram": repo["acc"],
            "repo_ngram": repo["repo"],
            "desc": repo["desc"],
        }


repo_dataset = sayt.DataSet(
    dir_index=dir_repo_index,
    index_name="repo",
    fields=repo_fields,
    cache=search_cache,
    cache_key="repo_dataset",
    cache_expire=30 * 24 * 60 * 60,  # 30 days
    cache_tag="repo_dataset",
    downloader=downloader,
)
