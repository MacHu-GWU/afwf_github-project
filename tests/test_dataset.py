# -*- coding: utf-8 -*-

from afwf_github.dataset import make_repo_dataset

FAKE_REPOS = [
    {"acc": "alice", "repo": "my-repo", "desc": "A personal project"},
    {"acc": "alice", "repo": "another-repo", "desc": "Another project"},
    {"acc": "acme", "repo": "acme-lib", "desc": "Shared Acme library"},
]


def test_search_by_repo_name(tmp_path):
    with make_repo_dataset(tmp_path, lambda: FAKE_REPOS, cache_expire=3600) as ds:
        result = ds.search("my-repo")
        assert result.size >= 1
        assert any(h.source["repo"] == "my-repo" for h in result.hits)


def test_search_by_account(tmp_path):
    with make_repo_dataset(tmp_path, lambda: FAKE_REPOS, cache_expire=3600) as ds:
        result = ds.search("acme")
        assert result.size >= 1
        assert all(h.source["acc"] == "acme" for h in result.hits)


def test_search_by_description(tmp_path):
    with make_repo_dataset(tmp_path, lambda: FAKE_REPOS, cache_expire=3600) as ds:
        result = ds.search("shared")
        assert result.size >= 1
        assert result.hits[0].source["repo"] == "acme-lib"


if __name__ == "__main__":
    from afwf_github.tests import run_cov_test

    run_cov_test(
        __file__,
        "afwf_github.dataset",
        preview=False,
    )
