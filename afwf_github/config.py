# -*- coding: utf-8 -*-

import json
from pathlib import Path
from functools import cached_property

from pydantic import BaseModel, ConfigDict
from github import Github, Auth

from .paths import path_enum

path_config_json = path_enum.path_config_json


class Config(BaseModel):
    model_config = ConfigDict(extra="forbid")

    pac_token: str
    cache_expire: int = 30 * 24 * 3600

    @classmethod
    def load(cls, path: Path) -> "Config":  # pragma: no cover
        return cls.model_validate(json.loads(path.read_text()))

    def dump(self, path: Path):  # pragma: no cover
        path.write_text(self.model_dump_json(indent=4))

    @cached_property
    def gh(self):
        return Github(auth=Auth.Token(self.pac_token))
