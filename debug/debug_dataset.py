# -*- coding: utf-8 -*-

from afwf_github.dataset import create_repo_dataset
from afwf_github.paths import path_enum
from afwf_github.config import Config
from rich import print as rprint

query = "afwf"

if __name__ == "__main__":
    config = Config.load(path_enum.path_config_json)
    repo_dataset = create_repo_dataset(config)
    res = repo_dataset.search(query=query)
    rprint(res)
