# -*- coding: utf-8 -*-

from configparser import ConfigParser
from pathlib_mate import Path

# def get_os_():


abspath = "/Users/sanhehu/Documents/GitHub/afwf_github-project/afwf_github/hdl/rebuild_index.py"
p_input: Path = Path(abspath)

found_p_git_config = False
p_git_config: Path = Path()
for p in p_input.parents:
    p_git_config = Path(p, ".git", "config")
    if p_git_config.exists():
        found_p_git_config = True
        break

if found_p_git_config is False:
    raise FileNotFoundError

config = ConfigParser()
config.read(p_git_config.abspath)
remote_url = config['remote "origin"']["url"]
repo_url = remote_url.replace(".git", "")


