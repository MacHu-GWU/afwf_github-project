# -*- coding: utf-8 -*-

import afwf
from .hdl import (
    repo,
    rebuild_index,
    rebuild_index_action,
)

wf = afwf.Workflow()
wf.register(repo.handler)
wf.register(rebuild_index.handler)
wf.register(rebuild_index_action.handler)
