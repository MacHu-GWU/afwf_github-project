# -*- coding: utf-8 -*-

import json
import dataclasses

from .paths import path_config_json


@dataclasses.dataclass
class Config:
    pac_token: str = dataclasses.field(default="your-github-personal-access-token-here")
    cache_expire: int = dataclasses.field(default=30 * 24 * 3600)

    @classmethod
    def load(cls):
        if path_config_json.exists():
            return cls(**json.loads(path_config_json.read_text()))
        else:
            config = cls()
            config.dump()
            return config

    def dump(self):
        path_config_json.write_text(json.dumps(dataclasses.asdict(self), indent=4))


config = Config.load()
