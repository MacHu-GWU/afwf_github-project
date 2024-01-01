# -*- coding: utf-8 -*-

from afwf_github.github import (
    create_gh_client,
    download_data,
    get_user,
    get_accounts,
    get_repos,
)
from rich import print as rprint

# page_limit = 3
page_limit = 9999

gh = create_gh_client()
download_data(gh, page_limit=page_limit, verbose=True)

user = get_user()
rprint(user)

accounts = get_accounts()
rprint(accounts[:10])

repos = get_repos()
rprint(repos[:10])
