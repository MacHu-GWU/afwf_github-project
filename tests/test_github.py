# -*- coding: utf-8 -*-

import json
import pytest

from afwf_github.constants import CacheKeyEnum
from afwf_github.github import (
    take,
    get_user,
    get_accounts,
    get_repos,
)

USERNAME = "alice"


def test_take():
    assert take([0, 1, 2, 3], 2) == [0, 1]
    assert take([0, 1, 2, 3], 0) == []
    assert take([0, 1, 2, 3], 99) == [0, 1, 2, 3]
    assert take(iter(range(5)), 3) == [0, 1, 2]


def test_cache_key_enum_values():
    assert CacheKeyEnum.user == "user"
    assert CacheKeyEnum.accounts == "accounts"
    assert CacheKeyEnum.repos == "repos"


def test_cache_key_enum_of():
    assert CacheKeyEnum.user.of(USERNAME) == "user@alice"
    assert CacheKeyEnum.accounts.of(USERNAME) == "accounts@alice"
    assert CacheKeyEnum.repos.of(USERNAME) == "repos@alice"


class TestGetters:
    @pytest.fixture
    def mock_cache(self):
        user = {"id": USERNAME, "name": "Alice"}
        accounts = [{"id": USERNAME, "name": "Alice"}, {"id": "acme", "name": "Acme"}]
        repos = [
            {"acc": USERNAME, "repo": "my-repo", "desc": "A repo"},
            {"acc": "acme", "repo": "acme-repo", "desc": ""},
        ]
        return {
            CacheKeyEnum.user.of(USERNAME): json.dumps(user),
            CacheKeyEnum.accounts.of(USERNAME): json.dumps(accounts),
            CacheKeyEnum.repos.of(USERNAME): json.dumps(repos),
        }

    def test_get_user(self, mock_cache):
        user = get_user(mock_cache, USERNAME)
        assert user["id"] == USERNAME
        assert user["name"] == "Alice"

    def test_get_accounts(self, mock_cache):
        accounts = get_accounts(mock_cache, USERNAME)
        assert len(accounts) == 2
        assert accounts[0]["id"] == USERNAME
        assert accounts[1]["id"] == "acme"

    def test_get_repos(self, mock_cache):
        repos = get_repos(mock_cache, USERNAME)
        assert len(repos) == 2
        assert repos[0]["acc"] == USERNAME
        assert repos[0]["repo"] == "my-repo"


if __name__ == "__main__":
    from afwf_github.tests import run_cov_test

    run_cov_test(
        __file__,
        "afwf_github.github",
        preview=False,
    )
