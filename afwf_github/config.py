# -*- coding: utf-8 -*-

import json
from pathlib import Path

from pydantic import BaseModel, ConfigDict

from .paths import path_enum

path_config_json = path_enum.path_config_json


class Config(BaseModel):
    model_config = ConfigDict(extra="forbid")

    pac_token: str
    cache_expire: int = 30 * 24 * 3600

    @classmethod
    def load(cls, path: Path) -> "Config": # pragma: no cover
        return cls.model_validate(json.loads(path.read_text()))

    def dump(self, path: Path): # pragma: no cover
        path.write_text(self.model_dump_json(indent=4))


