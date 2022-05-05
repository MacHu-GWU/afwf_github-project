# -*- coding: utf-8 -*-

"""
Given a absolute path of local file, find the corresponding web url.

Currently support:

- GitHub
- GitLab
"""

import attr
import afwf

from configparser import ConfigParser
from pathlib_mate import Path

from urllib.parse import urlparse


def convert_remote_origin_url_to_web_url(url: str) -> str:
    """
    """
    parse_result = urlparse(url)
    path = parse_result.path
    if path.startswith("/"):
        path = path[1:]
    if path.endswith(".git"):
        path = path[:-4]

    endpoint = parse_result.netloc.split("@")[-1]
    if ":" in endpoint:
        domain, port = endpoint.split(":", 1)
        endpoint = domain
        if domain in ["github.com", "gitlab.com"]:
            path = f"{port}/{path}"

    new_url = f"https://{endpoint}/{path}"
    return new_url


class NotGitRepoError(Exception): pass


def find_web_url(
    file_path: str,
    repo_dir: str,
    repo_url: str,
    git_branch: str,
    is_file: bool,
):
    file_path: Path = Path(file_path)
    repo_dir: Path = Path(repo_dir)
    relative_path = str(file_path.relative_to(repo_dir))
    if is_file:
        url = f"{repo_url}/blob/{git_branch}/{relative_path}"
    else:
        url = f"{repo_url}/tree/{git_branch}/{relative_path}"
    return url


def convert_file_path_to_web_url(
    abspath: str,
) -> str:
    """
    Given a file path on local laptop, find the corresponding web url.
    """
    path_input: Path = Path(abspath)

    found_dir_git_root = False
    dir_git_root: Path = Path()
    for p in path_input.parents:
        p_git_config = Path(p, ".git", "config")
        if p_git_config.exists():
            found_dir_git_root = True
            dir_git_root = p
            break

    if found_dir_git_root is False:
        raise NotGitRepoError

    config = ConfigParser()
    config.read(Path(dir_git_root, ".git", "config").abspath)
    remote_origin_url = config['remote "origin"']["url"]
    repo_web_url = convert_remote_origin_url_to_web_url(remote_origin_url)

    current_branch = Path(dir_git_root, ".git", "HEAD").read_text().strip().replace("ref: refs/heads/", "")

    file_web_url = find_web_url(
        file_path=path_input.abspath,
        repo_dir=dir_git_root.abspath,
        repo_url=repo_web_url,
        git_branch=current_branch,
        is_file=path_input.is_file(),
    )

    return file_web_url


@attr.define
class Handler(afwf.Handler):
    def lower_level_api(self, query: str) -> afwf.ScriptFilter:
        """
        """
        sf = afwf.ScriptFilter()

        if not query.strip():
            item = afwf.Item(
                title="Paste full path of a file or dir here",
            )
            sf.items.append(item)
            return sf

        try:
            url = convert_file_path_to_web_url(abspath=query)
            item = afwf.Item(
                title="View file in browser",
                subtitle=f"open {url}",
                arg=url,
            )
            item.open_url(url)
            sf.items.append(item)
        except NotGitRepoError:
            item = afwf.Item(
                title="It's not in any git repo directory",
                icon=afwf.Icon.from_image_file(afwf.Icons.error),
            )
            sf.items.append(item)
        return sf

    def handler(self, query: str) -> afwf.ScriptFilter:
        return self.lower_level_api(query=query)


handler = Handler(id="view_in_browser")
