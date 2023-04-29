from typing import AnyStr, List
from pydantic import BaseSettings, Extra, Field

class Time(BaseSettings):
    hour: int = Field(0, alias="HOUR")
    minute: int = Field(0, alias="MINUTE")

    class Config:
        extra = "allow"
        case_sensitive = False
        anystr_lower = True


class Config(BaseSettings):
    # plugin custom config
    plugin_setting: str = "default"

    todo_users: List[str] = []
    todo_groups: List[str] = []

    todo_send_time: List[Time] = []
    todo_keywords: List[str] = []

    class Config:
        extra = Extra.allow
        case_sensitive = False
