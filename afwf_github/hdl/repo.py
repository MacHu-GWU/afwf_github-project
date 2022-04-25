# -*- coding: utf-8 -*-

from typing import List, Dict, Iterable

import attr
import afwf

from ..fts import search_repo


@attr.define
class Handler(afwf.Handler):
    def lower_level_api(self, query: str) -> afwf.ScriptFilter:
        """

        :param kwargs:
        :return:
        """
        sf = afwf.ScriptFilter()
        if not query.strip():
            sf.items.append(afwf.Item(
                title="Type to search repository ...",
            ))
            return sf

        repos = search_repo(query)
        if len(repos) == 0:
            sf.items.append(afwf.Item(
                title="No result found!",
                icon=afwf.Icon.from_image_file(afwf.Icons.error)
            ))
        else:
            for repo in repos:
                account_name = repo["acc"]
                repo_name = repo["repo"]
                repo_description = repo.get("desc", "No description")
                url = f"https://github.com/{account_name}/{repo_name}"
                item = afwf.Item(
                    title=f"{account_name}/{repo_name}",
                    subtitle=repo_description,
                    autocomplete=f"{account_name}/{repo_name}",
                    arg=url,
                )
                item.open_url(url)
                sf.items.append(item)
        return sf

    def handler(self, query: str) -> afwf.ScriptFilter:
        return self.lower_level_api(query=query)


handler = Handler(id="repo")
