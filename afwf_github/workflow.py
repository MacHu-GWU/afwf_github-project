# -*- coding: utf-8 -*-

"""
workflow handler register.
"""

import afwf

from .handlers import (
    config,
    repo,
    rebuild_index,
    rebuild_index_action,
    view_in_browser,
)

wf = afwf.Workflow()
wf.register(config.handler)
wf.register(repo.handler)
wf.register(rebuild_index.handler)
wf.register(rebuild_index_action.handler)
wf.register(view_in_browser.handler)
