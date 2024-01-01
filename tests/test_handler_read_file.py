# -*- coding: utf-8 -*-

from afwf_github.handlers.read_file import handler, path_file


def test():
    sf = handler.handler("")
    assert len(sf.items) == 1
    assert sf.items[0].subtitle == path_file.read_text()


if __name__ == "__main__":
    from afwf_github.tests import run_cov_test

    run_cov_test(__file__, "afwf_github.handlers.read_file", preview=False)
