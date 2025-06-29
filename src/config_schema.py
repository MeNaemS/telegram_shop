from typing import Literal, List
from dataclasses import dataclass


@dataclass(slots=True)
class Database:
    host: str
    port: int
    name: str
    user: str
    password: str


@dataclass(slots=True)
class Telegram:
    token: str
    chats_id: List[str]


@dataclass(slots=True)
class Config:
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    debug: bool
    database: Database
    telegram: Telegram
