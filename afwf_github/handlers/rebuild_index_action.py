# -*- coding: utf-8 -*-

import typing as T

import attr
import afwf

from ..dataset import repo_dataset


@attr.define
class Handler(afwf.Handler):
    def main(self) -> afwf.ScriptFilter:
        repo_dataset.search(query="", refresh_data=True, verbose=False)
        return afwf.ScriptFilter()

    def parse_query(self, query: str) -> T.Dict[str, T.Any]:
        return {}

    def encode_query(self, **kwargs) -> str:
        return ""


handler = Handler(id="rebuild_index_action")
