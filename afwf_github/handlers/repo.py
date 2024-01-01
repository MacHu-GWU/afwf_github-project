# -*- coding: utf-8 -*-

import typing as T

import attrs
import afwf.api as afwf

from ..dataset import repo_dataset


@attrs.define
class Handler(afwf.Handler):
    def main(self, query: str) -> afwf.ScriptFilter:
        """

        :param kwargs:
        :return:
        """
        sf = afwf.ScriptFilter()

        if not query.strip():
            sf.items.append(
                afwf.Item(
                    title="Type to search GitHub repository ...",
                )
            )
            return sf

        repos = repo_dataset.search(
            query, limit=50, simple_response=True, verbose=False
        )

        if len(repos) == 0:
            sf.items.append(
                afwf.Item(
                    title="No result found!",
                    icon=afwf.Icon.from_image_file(afwf.IconFileEnum.error),
                )
            )
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

    def parse_query(self, query: str) -> T.Dict[str, T.Any]:
        return dict(query=query)


handler = Handler(id="repo")
