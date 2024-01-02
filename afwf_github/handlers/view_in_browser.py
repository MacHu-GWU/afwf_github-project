# -*- coding: utf-8 -*-

"""
Given an absolute path of local file, find the corresponding web url.
"""

import typing as T
from pathlib import Path

import attrs
import git_web_url.api as gwu
from git_web_url.exc import NotGitRepoError
import afwf.api as afwf


@attrs.define
class Handler(afwf.Handler):
    def main(self, path: str) -> afwf.ScriptFilter:
        """ """
        sf = afwf.ScriptFilter()

        if not path.strip():
            item = afwf.Item(
                title="Paste full path of a file or dir here",
            )
            sf.items.append(item)
            return sf

        try:
            url = gwu.get_web_url(Path(path))
            item = afwf.Item(
                title=f"View {path} in browser",
                subtitle=f"open {url}",
                arg=url,
                icon=afwf.Icon.from_image_file(afwf.IconFileEnum.internet),
            )
            item.open_url(url)
            sf.items.append(item)
        except NotGitRepoError:
            item = afwf.Item(
                title="The file is not in a git repo directory",
                icon=afwf.Icon.from_image_file(afwf.IconFileEnum.error),
            )
            sf.items.append(item)
        return sf

    def parse_query(self, query: str) -> T.Dict[str, T.Any]:
        return dict(path=query)


handler = Handler(id="view_in_browser")
