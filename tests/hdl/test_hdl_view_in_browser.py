# -*- coding: utf-8 -*-

import pytest
from afwf_github.hdl.view_in_browser import (
    convert_remote_origin_url_to_web_url,
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
    assert web_url == "https://my.enterprise.com:1234/account-name/repo-name"


def test_convert_file_path_to_web_url():
    url = convert_file_path_to_web_url(__file__)
    assert url == "https://github.com/MacHu-GWU/afwf_github-project/blob/main/tests/hdl/test_hdl_view_in_browser.py"


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
