from typing import TypedDict

from server.models.server_cache_object import ServerCacheObject


class ServerCache(TypedDict):
    client_id: str
    cache_object: ServerCacheObject
