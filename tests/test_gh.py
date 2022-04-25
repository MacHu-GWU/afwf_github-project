# -*- coding: utf-8 -*-

import pytest
from afwf_github.runtime import IS_LOCAL
from afwf_github.gh import (
    refresh_cache, get_user, get_accounts, get_repos,
)
from afwf_github.tests import cache, build_test_cache


def setup_module(module):
    build_test_cache()


def test_get_xyz():
    assert len(get_accounts(cache)) == 5
    assert len(get_repos(cache)) == 9


def test_refresh_cache():
    if IS_LOCAL:
        from rich import print as rprint

        refresh_cache()
        get_user()
        get_accounts()
        get_repos()
        pass


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
