# -*- coding: utf-8 -*-

import pytest
from afwf_github.fts import (
    rebuild_org_index,
    search_org,
    rebuild_repo_index,
    search_repo,
)
from afwf_github.runtime import IS_LOCAL
from afwf_github.tests import (
    build_test_cache, build_test_index,
    dir_org_index_for_test as dir_org_index,
    dir_repo_index_for_test as dir_repo_index,
)
from rich import print as rprint


def setup_module(module):
    build_test_cache()
    build_test_index()


def test_search_org():
    res = search_org("ama", dir_org_index)
    assert len(res) == 1
    assert res[0]["id"] == "amzn"

    res = search_org("zon", dir_org_index)
    assert len(res) == 1
    assert res[0]["id"] == "amzn"


def test_search_repo():
    res = search_repo("amz", dir_repo_index)
    assert len(res) == 5

    res = search_repo("fin report", dir_repo_index)
    assert len(res) == 5

    res = search_repo("fin report amz", dir_repo_index)
    assert len(res) == 1
    assert res[0]["acc"] == "amzn"


def test_local():
    if IS_LOCAL:
        # rebuild_org_index()
        # rebuild_repo_index()
        # res = search_org("mac")
        # rprint(res)
        # res = search_repo("s3path")
        # rprint(res)
        pass


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
