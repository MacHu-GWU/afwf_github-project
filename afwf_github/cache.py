# -*- coding: utf-8 -*-

"""
Factory for diskcache instances used to store GitHub API responses.

Each GitHub user gets their own cache directory under their per-user data
directory. sayt2 datasets manage their own internal search result cache
separately — this module only covers GitHub API response caching.
"""

from pathlib import Path

from diskcache import Cache


def make_cache(dir_cache: Path) -> Cache:
    """Create a ``diskcache.Cache`` at *dir_cache*.

    diskcache creates the directory if it does not exist, so callers do not
    need to ensure the path exists beforehand.
    """
    return Cache(dir_cache)
