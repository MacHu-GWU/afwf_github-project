# -*- coding: utf-8 -*-

"""
Given a absolute path of local file, find the corresponding web url.

Currently support:

- GitHub
- GitLab
- BitBucket
- AWS CodeCommit
"""

from typing import Iterable, Tuple
import enum
from urllib.parse import urlparse
from configparser import ConfigParser

import attr
from attrs_mate import AttrsClass
import afwf
from giturlparse import parse
from pathlib_mate import Path


@attr.define
class GitSystem(AttrsClass):
    name: str = AttrsClass.ib_str()
    domain: str = AttrsClass.ib_str()


class GitSystemEnum(enum.Enum):
    unknown = GitSystem(name="unknown", domain="unknown.com")
    github = GitSystem(name="github", domain="github.com")
    gitlab = GitSystem(name="gitlab", domain="gitlab.com")
    bitbucket = GitSystem(name="bitbucket", domain="bitbucket.org")
    aws_codecommit = GitSystem(
        name="aws_codecommit", domain="git-codecommit.{region}.amazonaws.com"
    )

    @classmethod
    def iter_items(cls) -> Iterable[Tuple[str, "GitSystem"]]:
        for member in cls:
            yield member.name, member.value


@attr.define
class Url(AttrsClass):
    origin_url: str = AttrsClass.ib_str()
    web_url: str = AttrsClass.ib_str()
    git_sys: GitSystemEnum = AttrsClass.ib_generic(GitSystemEnum)


class UrlEnum(enum.Enum):
    github_saas_http = Url(
        origin_url="https://github.com/user-name/repo-name.git",
        web_url="https://github.com/user-name/repo-name",
        git_sys=GitSystemEnum.github,
    )
    github_saas_token = Url(
        origin_url="https://my_github_token@github.com/user-name/repo-name.git",
        web_url="https://github.com/user-name/repo-name",
        git_sys=GitSystemEnum.github,
    )
    github_saas_ssh = Url(
        origin_url="ssh://git@github.com:user-name/repo-name.git",
        web_url="https://github.com/user-name/repo-name",
        git_sys=GitSystemEnum.github,
    )

    gitlab_saas_http = Url(
        origin_url="https://gitlab.com/user-name/repo-name.git",
        web_url="https://gitlab.com/user-name/repo-name",
        git_sys=GitSystemEnum.gitlab,
    )
    gitlab_saas_token = Url(
        origin_url="https://oauth2:my_gitlab_token@gitlab.com/user-name/repo-name.git",
        web_url="https://gitlab.com/user-name/repo-name",
        git_sys=GitSystemEnum.gitlab,
    )
    gitlab_saas_ssh = Url(
        origin_url="ssh://git@gitlab.com:user-name/repo-name.git",
        web_url="https://gitlab.com/user-name/repo-name",
        git_sys=GitSystemEnum.gitlab,
    )

    gitlab_enterprise_http = Url(
        origin_url="https://my.enterprise.com/user-name/repo-name.git",
        web_url="https://my.enterprise.com/user-name/repo-name",
        git_sys=GitSystemEnum.unknown,
    )
    gitlab_enterprise_token = Url(
        origin_url="https://oauth2:my_gitlab_token@my.enterprise.com/user-name/repo-name",
        web_url="https://my.enterprise.com/user-name/repo-name",
        git_sys=GitSystemEnum.unknown,
    )
    gitlab_enterprise_ssh = Url(
        origin_url="ssh://git@my.enterprise.com:1234/user-name/repo-name.git",
        web_url="https://my.enterprise.com/user-name/repo-name",
        git_sys=GitSystemEnum.unknown,
    )

    bitbucket_saas_http = Url(
        origin_url="https://bitbucket.org/user-name/repo-name.git",
        # example: https://bitbucket.org/astanin/python-tabulate
        web_url="https://bitbucket.org/user-name/repo-name",
        git_sys=GitSystemEnum.bitbucket,
    )
    bitbucket_saas_ssh = Url(
        origin_url="git@bitbucket.org:user-name/repo-name.git",
        web_url="https://bitbucket.org/user-name/repo-name",
        git_sys=GitSystemEnum.bitbucket,
    )
    bitbucket_enterprise_http = Url(
        origin_url="https://account-name@bitbucket.prod.mycompany.com/user-name/repo-name.git",
        web_url="https://bitbucket.prod.mycompany.com/projects/user-name/repos/repo-name",
        git_sys=GitSystemEnum.unknown,
    )
    bitbucket_enterprise_ssh = Url(
        origin_url="ssh://git@bitbucket.prod.mycompany.com:7999/user-name/repo-name.git",
        web_url="https://bitbucket.prod.mycompany.com/projects/user-name/repos/repo-name",
        git_sys=GitSystemEnum.bitbucket,
    )

    aws_codecommit_http = Url(
        origin_url="https://git-codecommit.us-east-1.amazonaws.com/v1/repos/repo-name",
        web_url="https://us-east-1.console.aws.amazon.com/codesuite/codecommit/repositories/repo-name",
        git_sys=GitSystemEnum.aws_codecommit,
    )
    aws_codecommit_ssh = Url(
        origin_url="ssh://git-codecommit.us-east-1.amazonaws.com/v1/repos/repo-name",
        web_url="https://us-east-1.console.aws.amazon.com/codesuite/codecommit/repositories/repo-name",
        git_sys=GitSystemEnum.aws_codecommit,
    )
    aws_codecommit_grc = Url(
        origin_url="codecommit::us-east-1://repo-name",
        web_url="https://us-east-1.console.aws.amazon.com/codesuite/codecommit/repositories/repo-name",
        git_sys=GitSystemEnum.aws_codecommit,
    )

    @classmethod
    def iter_items(cls) -> Iterable[Tuple[str, "Url"]]:
        for member in cls:
            yield member.name, member.value

    @classmethod
    def iter_items_by_git_system(
        cls, git_system: GitSystemEnum
    ) -> Iterable[Tuple[str, "Url"]]:
        for member in cls:
            if member.value.git_sys.value.name == git_system.name:
                yield member.name, member.value

    @classmethod
    def iter_github_items(cls) -> Iterable[Tuple[str, "Url"]]:  # pragma: no cover
        yield from cls.iter_items_by_git_system(GitSystemEnum.github.value)

    @classmethod
    def iter_gitlab_items(cls) -> Iterable[Tuple[str, "Url"]]:  # pragma: no cover
        yield from cls.iter_items_by_git_system(GitSystemEnum.gitlab.value)

    @classmethod
    def iter_bitbucket_items(cls) -> Iterable[Tuple[str, "Url"]]:  # pragma: no cover
        yield from cls.iter_items_by_git_system(GitSystemEnum.bitbucket.value)

    @classmethod
    def iter_aws_codecommit_items(cls) -> Iterable[Tuple[str, "Url"]]:
        yield from cls.iter_items_by_git_system(GitSystemEnum.aws_codecommit.value)


def detect_git_system(url: str) -> GitSystemEnum:
    if url.startswith("https://github.com"):
        return GitSystemEnum.github
    elif "@github.com/" in url:
        return GitSystemEnum.github
    elif url.startswith("ssh://git@github.com:"):
        return GitSystemEnum.github

    elif url.startswith("https://gitlab.com"):
        return GitSystemEnum.gitlab
    elif "@gitlab.com/" in url:
        return GitSystemEnum.gitlab
    elif url.startswith("ssh://git@gitlab.com:"):
        return GitSystemEnum.gitlab

    elif url.startswith("https://bitbucket.org"):
        return GitSystemEnum.bitbucket
    elif url.startswith("git@bitbucket.org:"):
        return GitSystemEnum.bitbucket
    elif url.startswith("ssh://git@bitbucket"):
        return GitSystemEnum.bitbucket

    elif url.startswith("https://git-codecommit"):
        return GitSystemEnum.aws_codecommit
    elif url.startswith("ssh://git-codecommit"):
        return GitSystemEnum.aws_codecommit
    elif "codecommit::" in url:
        return GitSystemEnum.aws_codecommit

    else:
        return GitSystemEnum.unknown


def parse_aws_codecommit_url(url: str) -> Tuple[str, str]:
    """
    :param url:
    :return: region, repo_name
    """
    if url.startswith("https://git-codecommit") or url.startswith(
        "ssh://git-codecommit"
    ):
        parse_result = urlparse(url)
        region = parse_result.netloc.split(".")[1]
        repo_name = parse_result.path.split("/")[-1]
    elif url.startswith("codecommit::"):
        paths = url.split(":")
        region, repo_name = paths[-2], paths[-1].lstrip("//")
    else:
        raise NotImplementedError
    return region, repo_name


class NotGitRepoError(Exception):
    pass


def pretty_print_result(res):  # pragma: no cover
    """
    Pretty print giturlparser.parse returns.
    """
    print(f"platform = {res.platform!r}")
    print(f"host = {res.host!r}")
    print(f"resource = {res.resource!r}")
    print(f"port = {res.port!r}")
    print(f"protocol = {res.protocol!r}")
    print(f"protocols = {res.protocols!r}")
    print(f"user = {res.user!r}")
    print(f"owner = {res.owner!r}")
    print(f"repo = {res.repo!r}")
    print(f"name = {res.name!r}")
    print(f"groups = {res.groups!r}")
    print(f"path = {res.path!r}")
    print(f"path_raw = {res.path_raw!r}")
    print(f"branch = {res.branch!r}")


def find_web_url(url: str) -> str:
    # detect git system
    git_system = detect_git_system(url)

    # handler AWS Code Commit
    if git_system is GitSystemEnum.aws_codecommit:
        region, repo_name = parse_aws_codecommit_url(url)
        web_url = f"https://{region}.console.aws.amazon.com/codesuite/codecommit/repositories/{repo_name}"

    # handler github, gitlab, bitbucket
    else:
        res = parse(url)
        # pretty_print_result(res)
        if "@" in res.host:
            host = res.host.split("@")[-1]
        else:
            host = res.host
        if host.startswith("bitbucket.") and (not host.startswith("bitbucket.org")):
            web_url = f"https://{host}/projects/{res.owner}/repos/{res.name}"
        else:
            web_url = f"https://{host}/{res.owner}/{res.name}"
    # print(web_url)
    return web_url


def find_browse_url(
    file_path: str,
    repo_dir: str,
    origin_url: str,
    web_url: str,
    git_branch: str,
    is_file: bool,
) -> str:
    file_path: Path = Path(file_path)
    repo_dir: Path = Path(repo_dir)
    relative_path = str(file_path.relative_to(repo_dir))
    if "console.aws.amazon.com/codesuite/codecommit" in web_url:
        region, _ = parse_aws_codecommit_url(origin_url)
        browser_url = f"{web_url}/browse/refs/heads/{git_branch}/--/{relative_path}?region={region}"
    elif (
        origin_url.startswith("https://") and "@bitbucket.org" in origin_url
        or origin_url.startswith("git@bitbucket.org")
    ):
        browser_url = f"{web_url}/src/{git_branch}/{relative_path}"
    elif (
        origin_url.startswith("https://") and "@bitbucket" in origin_url
    ) or origin_url.startswith("ssh://git@bitbucket"):
        browser_url = f"{web_url}/browse/{relative_path}?at=refs/heads/{git_branch}"
    else:
        if is_file:
            browser_url = f"{web_url}/blob/{git_branch}/{relative_path}"
        else:
            browser_url = f"{web_url}/tree/{git_branch}/{relative_path}"
    return browser_url


def convert_file_path_to_browse_url(
    abspath: str,
) -> str:
    """
    Given a file path on local laptop, find the corresponding browser url.
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
    remote_web_url = find_web_url(remote_origin_url)

    current_branch = (
        Path(dir_git_root, ".git", "HEAD")
        .read_text()
        .strip()
        .replace("ref: refs/heads/", "")
    )

    browse_url = find_browse_url(
        file_path=path_input.abspath,
        repo_dir=dir_git_root.abspath,
        origin_url=remote_origin_url,
        web_url=remote_web_url,
        git_branch=current_branch,
        is_file=path_input.is_file(),
    )

    return browse_url


@attr.define
class Handler(afwf.Handler):
    def lower_level_api(self, query: str) -> afwf.ScriptFilter:
        """ """
        sf = afwf.ScriptFilter()

        if not query.strip():
            item = afwf.Item(
                title="Paste full path of a file or dir here",
            )
            sf.items.append(item)
            return sf

        try:
            url = convert_file_path_to_browse_url(abspath=query)
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
