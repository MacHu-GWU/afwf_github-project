# -*- coding: utf-8 -*-

import pytest
from afwf_github.config import Config


def test_config_required_fields():
    config = Config(pac_token="my-token")
    assert config.pac_token == "my-token"
    assert config.cache_expire == 30 * 24 * 3600


def test_config_custom_values():
    config = Config(pac_token="my-token", cache_expire=3600)
    assert config.pac_token == "my-token"
    assert config.cache_expire == 3600


def test_config_pac_token_is_required():
    with pytest.raises(Exception):
        Config()


def test_config_extra_field_forbidden():
    with pytest.raises(Exception):
        Config(pac_token="tok", unknown_field="bad")


if __name__ == "__main__":
    from afwf_github.tests import run_cov_test

    run_cov_test(
        __file__,
        "afwf_github.config",
        preview=False,
    )
