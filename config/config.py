from dataclasses import dataclass

import dacite
import toml

from config.app import APP
from config.reminder import REMINDER
from config.stream import STREAM


@dataclass
class Config:
    APP: APP
    REMINDER: REMINDER
    STREAM: STREAM


config = dacite.from_dict(Config, toml.load("config.toml"))
