# -*- coding: utf-8 -*-

import json
from automation.ops import path_bin_python, dir_workflow
from afwf_github.handlers import (
    config,
    repo,
    rebuild_index,
    rebuild_index_action,
)
from rich import print as rprint

verbose = True
# verbose = False

# handler = config.handler

# handler = repo.handler

handler = rebuild_index.handler
query = ""

# handler = rebuild_index_action.handler

res = handler.run_script_command(path_bin_python, dir_workflow, query, verbose=verbose)
if res is None:
    print(f"res = {res}")
else:
    rprint(json.loads(res))
