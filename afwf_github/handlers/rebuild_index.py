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
        cmd = rebuild_index_action.handler.encode_run_script_command(
            bin_python=path_python_interpreter,
        )
        afwf.log_debug_info(f"will run command: {cmd}")
        item = afwf.Item(
            title="Rebuild Index for GitHub Alfred Workflow",
            subtitle="Hit enter to rebuild, it may takes 10 ~ 20 seconds",
            icon=afwf.Icon.from_image_file(afwf.IconFileEnum.reset)
        ).run_script(cmd)
        sf.items.append(item)
        return sf

    def parse_query(self, query: str) -> T.Dict[str, T.Any]:
        return {}


handler = Handler(id="rebuild_index")
