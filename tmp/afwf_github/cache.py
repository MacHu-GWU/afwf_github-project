# -*- coding: utf-8 -*-

"""
To avoid making too much GitHub API call, we use local cache to store
``list organization``, ``list repo`` results.
"""

from diskcache import Cache
from .paths import dir_cache

cache = Cache(dir_cache.abspath)
DEFAULT_EXPIRE = 30 * 24 * 3600
