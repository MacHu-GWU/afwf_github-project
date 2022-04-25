# -*- coding: utf-8 -*-

from diskcache import Cache
from ..paths import (
    dir_cache_for_test, path_org_json, path_repo_json,
    dir_org_index_for_test, dir_repo_index_for_test,
)
from ..cache import DEFAULT_EXPIRE
from ..fts import rebuild_org_index, rebuild_repo_index
from ..gh import CacheKeys

cache = Cache(dir_cache_for_test.abspath)


def build_test_cache():
    cache.set(CacheKeys.accounts, path_org_json.read_text(), expire=DEFAULT_EXPIRE)
    cache.set(CacheKeys.repos, path_repo_json.read_text(), expire=DEFAULT_EXPIRE)


def build_test_index():
    rebuild_org_index(dir_index=dir_org_index_for_test, cache=cache)
    rebuild_repo_index(dir_index=dir_repo_index_for_test, cache=cache)
