
.. .. image:: https://readthedocs.org/projects/afwf-github/badge/?version=latest
    :target: https://afwf-github.readthedocs.io/en/latest/
    :alt: Documentation Status

.. image:: https://github.com/MacHu-GWU/afwf_github-project/workflows/CI/badge.svg
    :target: https://github.com/MacHu-GWU/afwf_github-project/actions?query=workflow:CI

.. .. image:: https://codecov.io/gh/MacHu-GWU/afwf_github-project/branch/main/graph/badge.svg
    :target: https://codecov.io/gh/MacHu-GWU/afwf_github-project

.. .. image:: https://img.shields.io/pypi/v/afwf-github.svg
    :target: https://pypi.python.org/pypi/afwf-github

.. .. image:: https://img.shields.io/pypi/l/afwf-github.svg
    :target: https://pypi.python.org/pypi/afwf-github

.. .. image:: https://img.shields.io/pypi/pyversions/afwf-github.svg
    :target: https://pypi.python.org/pypi/afwf-github

.. image:: https://img.shields.io/badge/Release_History!--None.svg?style=social
    :target: https://github.com/MacHu-GWU/afwf_github-project/blob/main/release-history.rst

.. image:: https://img.shields.io/badge/STAR_Me_on_GitHub!--None.svg?style=social
    :target: https://github.com/MacHu-GWU/afwf_github-project

------

.. .. image:: https://img.shields.io/badge/Link-Document-blue.svg
    :target: https://afwf-github.readthedocs.io/en/latest/

.. .. image:: https://img.shields.io/badge/Link-API-blue.svg
    :target: https://afwf-github.readthedocs.io/en/latest/py-modindex.html

.. .. image:: https://img.shields.io/badge/Link-Install-blue.svg
    :target: `install`_

.. image:: https://img.shields.io/badge/Link-GitHub-blue.svg
    :target: https://github.com/MacHu-GWU/afwf_github-project

.. image:: https://img.shields.io/badge/Link-Submit_Issue-blue.svg
    :target: https://github.com/MacHu-GWU/afwf_github-project/issues

.. image:: https://img.shields.io/badge/Link-Request_Feature-blue.svg
    :target: https://github.com/MacHu-GWU/afwf_github-project/issues

.. image:: https://img.shields.io/badge/Link-Download-blue.svg
    :target: https://pypi.org/pypi/afwf-github#files


Welcome to ``afwf_github`` Documentation
==============================================================================
It is an `Alfred Workflow <https://www.alfredapp.com/workflows/>`_ for GitHub operations. There already is a PHP `alfred-github-workflow <https://github.com/gharlan/alfred-github-workflow>`_ library for this. But the searching is based on Alfred built-in word level filtering, which doesn't allow any typo, fuzzy, and full text search. This project aim to provide the best searching experience powered by the Single Machine, Pure Python version of ElasticSearch - `whoosh <https://pypi.org/project/Whoosh/>`_


Install
------------------------------------------------------------------------------
1. Make sure you have `Alfred 4 + <https://www.alfredapp.com/>`_ installed and bought the `Power Pack <https://www.alfredapp.com/shop/>`_.
2. Go to `Release <https://github.com/MacHu-GWU/afwf_github-project/releases>`_, download the latest release.
3. Double click the file to install.
4. Prepare your GitHub Personal Access Token: go to https://github.com/settings/tokens, create a new token, make sure you checked ``repo -> public_repo``, ``admin:org -> read:org``, ``admin:enterprise -> read:enterprise`` so the workflow can get your public repo name and url information. If you want to get your private repo as well, you should check ``repo (Full control of private repositories)``.


Usage
------------------------------------------------------------------------------
1. Configuration.

    In Alfred UI, type ``gh-config``, it should open the ~/.alfred-afwf/afwf_github/config.json``

    .. image:: https://github.com/MacHu-GWU/afwf_github-project/assets/6800411/2acff3ad-8a90-4326-8f64-3a54df2da11f

2. Build Index

    In Alfred UI, type ``gh-rebuild-index``, it should start to crawl your GitHub repos. It will take a while to finish. You can check the progress in the ``~/.alfred-afwf/afwf_github/.repo_index/``

    .. image:: https://github.com/MacHu-GWU/afwf_github-project/assets/6800411/59ce941d-a22a-4fb5-8013-c6a14ec5ca56

3. Search GitHub

    In Alfred UI, type ``gh ${query}``, it should show the following UI:

    .. image:: https://github.com/MacHu-GWU/afwf_github-project/assets/6800411/57ea7aa5-d2e0-4b73-8e66-632453418d92

4. Open Git Repo in Browser

    Copy any absolute path of a file in any git repo, type ``gh-view-in-browser ${path}`` then hit ``Enter``, it should open the repo in browser.

    .. image:: https://github.com/MacHu-GWU/afwf_github-project/assets/6800411/e863fac8-e9b0-4301-93c0-d745059e4346


Trouble Shooting
------------------------------------------------------------------------------
1. ``gh ${query}`` doesn't show any result.

    Check the ``${HOME}/.alfred-afwf/afwf_github/.repo_index`` folder, if the size is too small, it means the Workflow failed to crawl your GitHub repos. Please double check ``${HOME}/.alfred-afwf/afwf_github/config.json`` to make sure you have the correct GitHub Personal Access Token.
