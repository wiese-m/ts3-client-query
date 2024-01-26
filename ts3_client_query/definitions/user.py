from typing import NamedTuple

# todo: consider using attr/pydantic (for simple to/from dict methods and auto conversion)


class Myself(NamedTuple):
    client_id: int
    channel_id: int


class User(NamedTuple):
    client_id: int
    channel_id: int
    client_database_id: int
    client_nickname: str
    client_type: int
