# -*- coding: utf-8 -*-

from afwf_github.gh import gh, refresh_cache

# refresh_cache()

user = gh.get_user()
print(user.html_url)
# for o in user.get_orgs():
#     print(o)
# for repo in user.get_repos():
#     print(repo)
# for o in gh.get_organizations():
#     print(o)