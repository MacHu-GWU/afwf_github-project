# -*- coding: utf-8 -*-

from afwf_github.handlers.memorize_cache import handler


def test():
    sf1 = handler.main("key")
    sf2 = handler.main("key")
    assert sf1.items[0].title == sf2.items[0].title


if __name__ == "__main__":
    from afwf_github.tests import run_cov_test

    run_cov_test(__file__, "afwf_github.handlers.memorize_cache", preview=False)
