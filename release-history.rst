.. _release_history:

Release and Version History
==============================================================================


x.y.z (Planned)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

**Minor Improvements**

**Bugfixes**

**Miscellaneous**


1.0.4 (2026-06-14)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Minor Improvements**

- Normalize the search query in ``gh-search-repo`` by splitting on any non-alphanumeric
  character (hyphens, underscores, dots, spaces, etc.) before querying the index. This
  means typing ``abc-efg-def`` now matches repositories containing all three tokens
  individually instead of treating the entire string as one term.


1.0.3 (2026-05-16)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Bugfixes**

- Fix a bug where ``gh-rebuild-index`` did not fetch new repositories from GitHub. The
  downloader was returning stale data from diskcache even when a forced rebuild was
  requested, so newly created repos never appeared without manually deleting the cache
  directory. The ``rebuild-index-action`` now bypasses the diskcache and always pulls
  fresh data from the GitHub API.


1.0.2 (2026-05-09)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Bugfixes**

- Fix a bug that forgot to add url to arg when doing gh-view-in-browser.


1.0.1 (2026-04-21)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- Fully rework with AI.
- migrate from `sayt <https://pypi.org/project/sayt/>`_ to `sayt2 <https://pypi.org/project/sayt2/>`_.
- Use uv to distribute this Alfred workflow.


0.1.2 (2024-02-20)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Minor Improvements**

- Removed fuzzywuzzy python-levenstein from requirements.txt.

**Miscellaneous**

- Since this workflow depends on PyGitHub, it depends on cryptography library, which has C dependencies, so there's no way to make it pure Python.


0.1.1 (2024-01-01)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- Rework the implementation.
- Add ``gh-config`` command to manage configuration.
- Drop support for Python3.7, now only support Python3.8+.

**Minor Improvements**

- Fully adopt ``afwf==0.6.1`` for workflow development.
- Use ``sayt==0.6.5`` to power the search-as-you-type feature.
- Use ``git_web_url==0.1.3`` to power the ``gh-view-in-browser`` feature.


0.0.3 (2022-07-02)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- ``gh-view-in-browser`` now support GitHub SAAS, GitHub Enterprise, GitLab SAAS, GitLab Enterprise, BitBucket SAAS, BitBucket Enterprise, AWS CodeCommit


0.0.2 (2022-04-25)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- Add ``gh-view-in-browser`` keyword, add ``view_in_browser`` handler, allow to open local file in web browser.


0.0.1 (2022-04-24)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- First release.
- Add ``gh`` keyword, add ``repo`` handler, allow to search Github repository.
- Add ``gh-rebuild-index``keyword, add ``rebuild_index`` and ``rebuild_index_action`` handler, allow to rebuild GitHub search index.

**Miscellaneous**

- Support only 3.7+
