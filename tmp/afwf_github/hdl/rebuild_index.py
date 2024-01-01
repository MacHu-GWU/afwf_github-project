# -*- coding: utf-8 -*-

import attr
import afwf

from ..paths import path_python_interpreter

py_interpreter_path = path_python_interpreter.read_text().strip()


@attr.define
class Handler(afwf.Handler):
    def lower_level_api(self, query: str) -> afwf.ScriptFilter:
        """
        """
        sf = afwf.ScriptFilter()
        cmd = f"{py_interpreter_path} main.py 'rebuild_index_action no_query'"
        item = afwf.Item(
            title="Rebuild Index for GitHub Alfred Workflow",
            subtitle="Hit enter to rebuild, it may takes 10 ~ 20 seconds",
            arg=cmd,
            icon=afwf.Icon.from_image_file(afwf.Icons.reset)
        )
        item.terminal_command(cmd)
        sf.items.append(item)
        return sf

    def handler(self, query: str) -> afwf.ScriptFilter:
        return self.lower_level_api(query=query)


handler = Handler(id="rebuild_index")
