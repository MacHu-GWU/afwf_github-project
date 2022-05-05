# -*- coding: utf-8 -*-

import pytest
from afwf_github.hdl.view_in_browser import (
    convert_remote_origin_url_to_web_url,
    find_web_url,
    convert_file_path_to_web_url,
)


def test_convert_remote_origin_url_to_web_url():
    # --- GitHub
    # GitHub SAAS with username password
    url = "https://github.com/user-name/repo-name.git"
    web_url = convert_remote_origin_url_to_web_url(url)
    assert web_url == "https://github.com/user-name/repo-name"

    # GitHub SAAS with token
    url = "https://my_github_token@github.com/user-name/repo-name.git"
    web_url = convert_remote_origin_url_to_web_url(url)
    assert web_url == "https://github.com/user-name/repo-name"

    # GitHub SAAS with ssh
    url = "ssh://git@github.com:user-name/repo-name.git"
    web_url = convert_remote_origin_url_to_web_url(url)
    assert web_url == "https://github.com/user-name/repo-name"

    # --- GitLab
    # GitLab SAAS with username password
    url = "https://gitlab.com/user-name/repo-name.git"
    web_url = convert_remote_origin_url_to_web_url(url)
    assert web_url == "https://gitlab.com/user-name/repo-name"

    # GitLab SAAS with token
    url = "https://oauth2:my_gitlab_token@gitlab.com/user-name/repo-name.git"
    web_url = convert_remote_origin_url_to_web_url(url)
    assert web_url == "https://gitlab.com/user-name/repo-name"

    # GitLab SAAS with ssh
    url = "ssh://git@gitlab.com:user-name/repo-name.git"
    web_url = convert_remote_origin_url_to_web_url(url)
    assert web_url == "https://gitlab.com/user-name/repo-name"

    # --- GitLab enterprise
    # GitLab enterprise with token
    url = "https://oauth2:my_gitlab_token@my.enterprise.com/account-name/repo-name"
    web_url = convert_remote_origin_url_to_web_url(url)
    assert web_url == "https://my.enterprise.com/account-name/repo-name"

    # GitLab enterprise with SSH
    url = "ssh://git@my.enterprise.com:1234/account-name/repo-name.git"
    web_url = convert_remote_origin_url_to_web_url(url)
    assert web_url == "https://my.enterprise.com/account-name/repo-name"


def test_find_web_url():
    # GitHub SAAS
    assert find_web_url(
        file_path="/tmp/repo-name/folder/file.txt",
        repo_dir="/tmp/repo-name",
        repo_url="https://github.com/user-name/repo-name",
        git_branch="release/0.0.1",
        is_file=True,
    ) == "https://github.com/user-name/repo-name/blob/release/0.0.1/folder/file.txt"

    assert find_web_url(
        file_path="/tmp/repo-name/folder",
        repo_dir="/tmp/repo-name",
        repo_url="https://github.com/user-name/repo-name",
        git_branch="release/0.0.1",
        is_file=False,
    ) == "https://github.com/user-name/repo-name/tree/release/0.0.1/folder"

    # GitLab SAAS
    assert find_web_url(
        file_path="/tmp/repo-name/folder/file.txt",
        repo_dir="/tmp/repo-name",
        repo_url="https://gitlab.com/user-name/repo-name",
        git_branch="release/0.0.1",
        is_file=True,
    ) == "https://gitlab.com/user-name/repo-name/blob/release/0.0.1/folder/file.txt"

    # GitLab Enterprise
    assert find_web_url(
        file_path="/tmp/repo-name/folder/file.txt",
        repo_dir="/tmp/repo-name",
        repo_url="https://my.enterprise.com/account-name/repo-name",
        git_branch="release/0.0.1",
        is_file=True,
    ) == "https://my.enterprise.com/account-name/repo-name/blob/release/0.0.1/folder/file.txt"


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
