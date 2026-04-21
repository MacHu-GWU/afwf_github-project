# -*- coding: utf-8 -*-

import json
from pathlib import Path
from functools import cached_property

from pydantic import BaseModel, ConfigDict, model_validator
from github import Github, Auth
from home_secret_toml.api import hs

from .paths import path_enum

path_config_json = path_enum.path_config_json


class Config(BaseModel):
    model_config = ConfigDict(extra="forbid")

    pac_token: str | None = None
    pac_token_home_secret_toml_path: str | None = None
    cache_expire: int = 30 * 24 * 3600

    @model_validator(mode="after")
    def check_pac_token(self):
        if self.pac_token is None and self.pac_token_home_secret_toml_path is None:
            raise ValueError("Must provide pac_token or pac_token_home_secret_toml_path")
        return self

    @classmethod
    def load(cls, path: Path) -> "Config":  # pragma: no cover
        return cls.model_validate(json.loads(path.read_text()))

    def dump(self, path: Path):  # pragma: no cover
        path.write_text(self.model_dump_json(indent=4))

    @cached_property
    def gh(self):
        if self.pac_token is not None:
            pac_token = self.pac_token
        elif self.pac_token_home_secret_toml_path is not None:
            pac_token = hs.v(self.pac_token_home_secret_toml_path)
        else:
            raise ValueError("Must provide pac_token or pac_token_home_secret_toml")
        return Github(auth=Auth.Token(pac_token))
