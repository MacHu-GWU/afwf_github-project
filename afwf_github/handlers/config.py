# -*- coding: utf-8 -*-

import typing as T

import attrs
import afwf.api as afwf

from ..paths import path_config_json


@attrs.define
class Handler(afwf.Handler):
    def main(self) -> afwf.ScriptFilter:
        sf = afwf.ScriptFilter()
        sf.items.append(
            afwf.Item(
                title="Open and Edit config.json ...",
                subtitle=f"Tap 'Enter' to open {path_config_json}",
                icon=afwf.Icon.from_image_file(afwf.IconFileEnum.file),
            ).open_file(str(path_config_json))
        )
        return sf

    def parse_query(self, query: str) -> T.Dict[str, T.Any]:
        return {}


handler = Handler(id="config")
