# -*- coding: utf-8 -*-

import pytest
from afwf_github.hdl.view_in_browser import (
    detect_git_system,
    parse_aws_codecommit_url,
    find_web_url,
    find_browse_url,
    UrlEnum,
)


def test_detect_git_system():
    # assert (
    #     detect_git_system(UrlEnum.github_saas_https.value.origin_url)
    #     is UrlEnum.github_saas_https.value.git_sys
    # )
    for url_name, url_enum in UrlEnum.iter_items():
        git_system = detect_git_system(url_enum.origin_url)
        assert git_system is url_enum.git_sys


def test_parse_aws_codecommit_url():
    for url_name, url_enum in UrlEnum.iter_aws_codecommit_items():
        region, repo_name = parse_aws_codecommit_url(url_enum.origin_url)
        assert (region, repo_name) == ("us-east-1", "repo-name")


def test_find_web_url():
    assert find_web_url(UrlEnum.aws_codecommit_grc.value.origin_url) == UrlEnum.aws_codecommit_grc.value.web_url
    assert find_web_url(UrlEnum.aws_codecommit_http.value.origin_url) == UrlEnum.aws_codecommit_http.value.web_url
    assert find_web_url(UrlEnum.aws_codecommit_ssh.value.origin_url) == UrlEnum.aws_codecommit_ssh.value.web_url
    assert find_web_url(
        UrlEnum.bitbucket_enterprise_ssh.value.origin_url) == UrlEnum.bitbucket_enterprise_ssh.value.web_url
    assert find_web_url(UrlEnum.bitbucket_saas_http.value.origin_url) == UrlEnum.bitbucket_saas_http.value.web_url
    assert find_web_url(UrlEnum.bitbucket_saas_ssh.value.origin_url) == UrlEnum.bitbucket_saas_ssh.value.web_url
    assert find_web_url(UrlEnum.github_saas_http.value.origin_url) == UrlEnum.github_saas_http.value.web_url
    assert find_web_url(UrlEnum.github_saas_ssh.value.origin_url) == UrlEnum.github_saas_ssh.value.web_url
    assert find_web_url(UrlEnum.github_saas_token.value.origin_url) == UrlEnum.github_saas_token.value.web_url
    assert find_web_url(UrlEnum.gitlab_enterprise_http.value.origin_url) == UrlEnum.gitlab_enterprise_http.value.web_url
    assert find_web_url(UrlEnum.gitlab_enterprise_ssh.value.origin_url) == UrlEnum.gitlab_enterprise_ssh.value.web_url
    assert find_web_url(
        UrlEnum.gitlab_enterprise_token.value.origin_url) == UrlEnum.gitlab_enterprise_token.value.web_url
    assert find_web_url(UrlEnum.gitlab_saas_http.value.origin_url) == UrlEnum.gitlab_saas_http.value.web_url
    assert find_web_url(UrlEnum.gitlab_saas_ssh.value.origin_url) == UrlEnum.gitlab_saas_ssh.value.web_url
    assert find_web_url(UrlEnum.gitlab_saas_token.value.origin_url) == UrlEnum.gitlab_saas_token.value.web_url


def test_find_browser_url():
    # GitHub SAAS
    for url_enum in [
        UrlEnum.github_saas_http,
        UrlEnum.github_saas_token,
        UrlEnum.github_saas_ssh,
    ]:
        assert find_browse_url(
            file_path="/tmp/repo-name/folder/file.txt",
            repo_dir="/tmp/repo-name",
            origin_url=url_enum.value.origin_url,
            web_url=find_web_url(url_enum.value.origin_url),
            git_branch="release/0.0.1",
            is_file=True,
        ) == "https://github.com/user-name/repo-name/blob/release/0.0.1/folder/file.txt"

        assert find_browse_url(
            file_path="/tmp/repo-name/folder",
            repo_dir="/tmp/repo-name",
            origin_url=url_enum.value.origin_url,
            web_url=find_web_url(url_enum.value.origin_url),
            git_branch="release/0.0.1",
            is_file=False,
        ) == "https://github.com/user-name/repo-name/tree/release/0.0.1/folder"

    # GitLab SAAS
    for url_enum in [
        UrlEnum.gitlab_saas_http,
        UrlEnum.gitlab_saas_token,
        UrlEnum.gitlab_saas_ssh,
    ]:
        assert find_browse_url(
            file_path="/tmp/repo-name/folder/file.txt",
            repo_dir="/tmp/repo-name",
            origin_url=url_enum.value.origin_url,
            web_url=find_web_url(url_enum.value.origin_url),
            git_branch="release/0.0.1",
            is_file=True,
        ) == "https://gitlab.com/user-name/repo-name/blob/release/0.0.1/folder/file.txt"

        assert find_browse_url(
            file_path="/tmp/repo-name/folder",
            repo_dir="/tmp/repo-name",
            origin_url=url_enum.value.origin_url,
            web_url=find_web_url(url_enum.value.origin_url),
            git_branch="release/0.0.1",
            is_file=False,
        ) == "https://gitlab.com/user-name/repo-name/tree/release/0.0.1/folder"

    # GitLab Enterprise
    for url_enum in [
        UrlEnum.gitlab_enterprise_http,
        UrlEnum.gitlab_enterprise_token,
        UrlEnum.gitlab_enterprise_ssh,
    ]:
        assert find_browse_url(
            file_path="/tmp/repo-name/folder/file.txt",
            repo_dir="/tmp/repo-name",
            origin_url=url_enum.value.origin_url,
            web_url=find_web_url(url_enum.value.origin_url),
            git_branch="release/0.0.1",
            is_file=True,
        ) == "https://my.enterprise.com/user-name/repo-name/blob/release/0.0.1/folder/file.txt"

        assert find_browse_url(
            file_path="/tmp/repo-name/folder",
            repo_dir="/tmp/repo-name",
            origin_url=url_enum.value.origin_url,
            web_url=find_web_url(url_enum.value.origin_url),
            git_branch="release/0.0.1",
            is_file=False,
        ) == "https://my.enterprise.com/user-name/repo-name/tree/release/0.0.1/folder"

    # BitBucket SAAS
    for url_enum in [
        UrlEnum.bitbucket_saas_http,
        UrlEnum.bitbucket_saas_ssh,
    ]:
        assert find_browse_url(
            file_path="/tmp/repo-name/folder/file.txt",
            repo_dir="/tmp/repo-name",
            origin_url=url_enum.value.origin_url,
            web_url=find_web_url(url_enum.value.origin_url),
            git_branch="release/0.0.1",
            is_file=True,
        ) == "https://bitbucket.org/user-name/repo-name/src/release/0.0.1/folder/file.txt"

        assert find_browse_url(
            file_path="/tmp/repo-name/folder",
            repo_dir="/tmp/repo-name",
            origin_url=url_enum.value.origin_url,
            web_url=find_web_url(url_enum.value.origin_url),
            git_branch="release/0.0.1",
            is_file=False,
        ) == "https://bitbucket.org/user-name/repo-name/src/release/0.0.1/folder"

    # BitBucket Enterprise
    for url_enum in [
        UrlEnum.bitbucket_enterprise_http,
        UrlEnum.bitbucket_enterprise_ssh,
    ]:
        assert find_browse_url(
            file_path="/tmp/repo-name/folder/file.txt",
            repo_dir="/tmp/repo-name",
            origin_url=url_enum.value.origin_url,
            web_url=find_web_url(url_enum.value.origin_url),
            git_branch="release/0.0.1",
            is_file=True,
        ) == "https://bitbucket.prod.mycompany.com/projects/user-name/repos/repo-name/browse/folder/file.txt?at=refs/heads/release/0.0.1"

        assert find_browse_url(
            file_path="/tmp/repo-name/folder",
            repo_dir="/tmp/repo-name",
            origin_url=url_enum.value.origin_url,
            web_url=find_web_url(url_enum.value.origin_url),
            git_branch="release/0.0.1",
            is_file=False,
        ) == "https://bitbucket.prod.mycompany.com/projects/user-name/repos/repo-name/browse/folder?at=refs/heads/release/0.0.1"

    # AWS CodeCommit
    for url_enum in [
        UrlEnum.aws_codecommit_http,
        UrlEnum.aws_codecommit_ssh,
        UrlEnum.aws_codecommit_grc,
    ]:
        assert find_browse_url(
            file_path="/tmp/repo-name/folder/file.txt",
            repo_dir="/tmp/repo-name",
            origin_url=url_enum.value.origin_url,
            web_url=find_web_url(url_enum.value.origin_url),
            git_branch="release/0.0.1",
            is_file=True,
        ) == "https://us-east-1.console.aws.amazon.com/codesuite/codecommit/repositories/repo-name/browse/refs/heads/release/0.0.1/--/folder/file.txt?region=us-east-1"

        assert find_browse_url(
            file_path="/tmp/repo-name/folder",
            repo_dir="/tmp/repo-name",
            origin_url=url_enum.value.origin_url,
            web_url=find_web_url(url_enum.value.origin_url),
            git_branch="release/0.0.1",
            is_file=False,
        ) == "https://us-east-1.console.aws.amazon.com/codesuite/codecommit/repositories/repo-name/browse/refs/heads/release/0.0.1/--/folder?region=us-east-1"


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
