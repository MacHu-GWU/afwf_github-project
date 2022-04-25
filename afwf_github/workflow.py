# -*- coding: utf-8 -*-

import afwf
from .hdl import repo

wf = afwf.Workflow()
wf.register(repo.handler)
