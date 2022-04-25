# -*- coding: utf-8 -*-

from afwf_github.gh import create_gh_client

gh = create_gh_client()
user = gh.get_user()
print(user.html_url)
