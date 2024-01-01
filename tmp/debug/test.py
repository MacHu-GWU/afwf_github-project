# -*- coding: utf-8 -*-

import json
from pathlib_mate import Path
from afwf_github.gh import create_gh_client

gh = create_gh_client()
user = gh.get_user()

for repo in user.get_repos(visibility="all"):
    print(repo.html_url)
