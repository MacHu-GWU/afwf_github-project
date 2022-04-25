.. image:: https://github.com/MacHu-GWU/afwf_github-project/workflows/CI/badge.svg
    :target: https://github.com/MacHu-GWU/afwf_github-project/actions?query=workflow:CI

.. image:: https://img.shields.io/badge/STAR_Me_on_GitHub!--None.svg?style=social
    :target: https://github.com/MacHu-GWU/afwf_github-project

------

.. image:: https://img.shields.io/badge/Link-GitHub-blue.svg
    :target: https://github.com/MacHu-GWU/afwf_github-project

.. image:: https://img.shields.io/badge/Link-Submit_Issue-blue.svg
    :target: https://github.com/MacHu-GWU/afwf_github-project/issues

.. image:: https://img.shields.io/badge/Link-Request_Feature-blue.svg
    :target: https://github.com/MacHu-GWU/afwf_github-project/issues


Welcome to ``afwf_github`` Documentation
==============================================================================

It is an `Alfred Workflow <https://www.alfredapp.com/workflows/>`_ for GitHub operations. There already is a PHP `alfred-github-workflow <https://github.com/gharlan/alfred-github-workflow>`_ library for this. But the searching is based on Alfred built-in word level filtering, which doesn't allow any typo, fuzzy, and full text search. This project aim to provide the best searching experience powered by the Single Machine, Pure Python version of ElasticSearch - `whoosh <https://pypi.org/project/Whoosh/>`_


Install
------------------------------------------------------------------------------
1. Make sure you have `Alfred 4 + <https://www.alfredapp.com/>`_ installed and bought the `Power Pack <https://www.alfredapp.com/shop/>`_.
2. Go to `Release <https://github.com/MacHu-GWU/afwf_github-project/releases>`_, download the latest release.
3. Double click the file to install.
4. Prepare your GitHub Personal Access Token: go to https://github.com/settings/tokens, create a new token, make sure you checked ``repo -> public_repo``, ``admin:org -> read:org``, ``admin:enterprise -> read:enterprise`` so the workflow can get your repo name and url information.
5. Setup the GitHub personal access token file and python interpreter config file. So the workflow knows where to read the token and which python to use.

.. code-block:: bash

    # Create data directory
    mkdir ~/.alfred-afwf_github

    # Create the GitHub Personal Access Token file
    # replace ${GITHUB_PERSONAL_ACCESS_TOKEN} with your token
    echo "${GITHUB_PERSONAL_ACCESS_TOKEN}" > ~/.alfred-afwf_github/default

    # Create the Python Interpreter file
    # Now it support Python3.7+ only
    # If you are using python3, you can use ``which python3`` command to find
    # the full path of Python interpreter
    # replace ${PYTHON_INTERPRETER_PATH} with the path
    echo "${PYTHON_INTERPRETER_PATH}" > ~/.alfred-afwf_github/python_interpreter
