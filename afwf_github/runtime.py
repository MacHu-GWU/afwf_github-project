# -*- coding: utf-8 -*-

import os


class Runtime:
    local = "local"
    ci = "ci"


IS_LOCAL = False
IS_CI = False

if "CI" in os.environ:
    CURRENT_RUNTIME = Runtime.ci
    IS_CI = True
else:
    CURRENT_RUNTIME = Runtime.local
    IS_LOCAL = True
