# -*- coding: utf-8 -*-

from afwf_github import api


def test():
    _ = api


if __name__ == "__main__":
    from afwf_github.tests import run_cov_test

    run_cov_test(
        __file__,
        "afwf_github.api",
        preview=False,
    )
