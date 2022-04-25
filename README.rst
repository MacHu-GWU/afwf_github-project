
.. image:: https://readthedocs.org/projects/afwf_github/badge/?version=latest
    :target: https://afwf_github.readthedocs.io/index.html
    :alt: Documentation Status

.. image:: https://github.com/MacHu-GWU/afwf_github-project/workflows/CI/badge.svg
    :target: https://github.com/MacHu-GWU/afwf_github-project/actions?query=workflow:CI

.. image:: https://codecov.io/gh/MacHu-GWU/afwf_github-project/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/MacHu-GWU/afwf_github-project

.. image:: https://img.shields.io/pypi/v/afwf_github.svg
    :target: https://pypi.python.org/pypi/afwf_github

.. image:: https://img.shields.io/pypi/l/afwf_github.svg
    :target: https://pypi.python.org/pypi/afwf_github

.. image:: https://img.shields.io/pypi/pyversions/afwf_github.svg
    :target: https://pypi.python.org/pypi/afwf_github

.. image:: https://img.shields.io/badge/STAR_Me_on_GitHub!--None.svg?style=social
    :target: https://github.com/MacHu-GWU/afwf_github-project

------


.. image:: https://img.shields.io/badge/Link-Document-blue.svg
    :target: https://afwf_github.readthedocs.io/index.html

.. image:: https://img.shields.io/badge/Link-API-blue.svg
    :target: https://afwf_github.readthedocs.io/py-modindex.html

.. image:: https://img.shields.io/badge/Link-Source_Code-blue.svg
    :target: https://afwf_github.readthedocs.io/py-modindex.html

.. image:: https://img.shields.io/badge/Link-Install-blue.svg
    :target: `install`_

.. image:: https://img.shields.io/badge/Link-GitHub-blue.svg
    :target: https://github.com/MacHu-GWU/afwf_github-project

.. image:: https://img.shields.io/badge/Link-Submit_Issue-blue.svg
    :target: https://github.com/MacHu-GWU/afwf_github-project/issues

.. image:: https://img.shields.io/badge/Link-Request_Feature-blue.svg
    :target: https://github.com/MacHu-GWU/afwf_github-project/issues

.. image:: https://img.shields.io/badge/Link-Download-blue.svg
    :target: https://pypi.org/pypi/afwf_github#files


Welcome to ``afwf_github`` Documentation
==============================================================================


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
