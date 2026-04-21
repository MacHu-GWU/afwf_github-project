---
name: git-web-url
description: Use git_web_url (gwu/gitweburl CLI) to get the browser URL or relative path of a local file in a git repo. Load this skill when the user wants to open a file/folder on GitHub/GitLab/Bitbucket/CodeCommit in their browser, or needs the relative repo path of a local file.
---

`git_web_url` is a CLI tool (commands: `gwu` or `gitweburl`) that prints the browser-clickable URL for any local file or folder inside a git repository. It supports GitHub, GitHub Enterprise, GitLab, GitLab Enterprise, BitBucket, BitBucket Enterprise, and AWS CodeCommit.

## Part 1: Core CLI Usage (`gwu` / `gitweburl`)

Both `gwu` and `gitweburl` are identical entry points.

### `url` subcommand — print the browser URL

```bash
# Current directory, current branch (default)
gwu url

# Specific file or folder (absolute path)
gwu url /path/to/repo/src/module/file.py

# Branch options via --branch flag
gwu url                          # current branch (default)
gwu url --branch=default         # repo default branch (main/master), URL without explicit branch
gwu url --branch=main            # specific branch by name
gwu url -b develop               # short form, also works
gwu url /path/to/file --branch=main
```

### `relpath` subcommand — print relative path from repo root

```bash
# Current directory
gwu relpath

# Specific path
gwu relpath /path/to/repo/src/module/file.py

# At repo root → prints "."
# In subdirectory → prints e.g. "src/module/file.py"
```

### Python API (if using as a library)

```python
from pathlib import Path
import git_web_url.api as gwu

url = gwu.get_web_url(Path("/path/to/repo/file.py"))                          # current branch
url = gwu.get_web_url(Path("/path/to/repo/file.py"), branch=gwu.DEFAULT_BRANCH)  # default branch
url = gwu.get_web_url(Path("/path/to/repo/file.py"), branch="feature-branch") # specific branch
```

## Part 2: One-off Usage with `uvx` (no install needed)

When `gwu`/`gitweburl` is not installed in the environment, use `uvx` to run the package directly:

```bash
# Pin to a specific version for reproducibility (recommended)
uvx --from git-web-url==<version> gwu url
uvx --from git-web-url==<version> gwu url /abs/path/to/file.py
uvx --from git-web-url==<version> gwu url --branch=main
uvx --from git-web-url==<version> gwu relpath /abs/path/to/file.py
```

`uvx` downloads and runs the package in an isolated environment with no side effects.

To find the latest stable version and release history, check:
https://raw.githubusercontent.com/MacHu-GWU/git_web_url-project/refs/heads/main/release-history.rst
