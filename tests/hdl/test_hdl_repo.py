# -*- coding: utf-8 -*-

import pytest
from rich import print as rprint
from afwf_github.runtime import IS_LOCAL
from afwf_github.hdl.repo import handler


def test():
    if IS_LOCAL:
        sf = handler.lower_level_api(query="mac dla")
        sf_dct = sf.to_script_filter()


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
