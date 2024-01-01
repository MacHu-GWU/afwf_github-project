# -*- coding: utf-8 -*-

from afwf_github.dataset import (
    repo_dataset,
)
from rich import print as rprint

query = "afwf"

if __name__ == "__main__":
    res = repo_dataset.search(query=query, verbose=True, simple_response=True)
    rprint(res)
