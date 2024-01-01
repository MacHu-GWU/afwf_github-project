# -*- coding: utf-8 -*-

import typing as T

import attrs
import afwf.api as afwf

from ..paths import path_python_interpreter

from . import rebuild_index_action


@attrs.define
class Handler(afwf.Handler):
    def main(self) -> afwf.ScriptFilter:
        sf = afwf.ScriptFilter()
        cmd = f"{path_python_interpreter} main.py 'rebuild_index_action no_query'"
        item = afwf.Item(
            title="Rebuild Index for GitHub Alfred Workflow",
            subtitle="Hit enter to rebuild, it may takes 10 ~ 20 seconds",
            arg=cmd,
            icon=afwf.Icon.from_image_file(afwf.IconFileEnum.reset)
        ).terminal_command(
            rebuild_index_action.handler.encode_run_script_command(
                bin_python=path_python_interpreter,
            )
        )
        sf.items.append(item)
        return sf

    def parse_query(self, query: str) -> T.Dict[str, T.Any]:
        return {}


handler = Handler(id="rebuild_index")
