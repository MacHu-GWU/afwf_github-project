# -*- coding: utf-8 -*-

"""
Disk cache for Alfred Workflow.
"""

from diskcache import Cache

from .paths import dir_cache, dir_search_cache

cache = Cache(dir_cache.abspath)
search_cache = Cache(dir_search_cache.abspath)
