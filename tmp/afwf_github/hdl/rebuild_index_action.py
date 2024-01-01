# -*- coding: utf-8 -*-

import attr
import afwf

from ..gh import refresh_cache
from ..fts import rebuild_org_index, rebuild_repo_index


@attr.define
class Handler(afwf.Handler):
    def handler(self, query: str) -> afwf.ScriptFilter:
        refresh_cache()
        rebuild_org_index()
        rebuild_repo_index()
        return afwf.ScriptFilter()


handler = Handler(id="rebuild_index_action")
