import json
from ctypes import Union

from dataclasses import dataclass
from typing import Tuple


@dataclass
class LogEvent:
    event: str
    server_address: str
    client_socket_id: str
    client_id: int
    value: str

    def __init__(self, event: str,
                 client_address: Tuple[str, str],
                 client_socket_id: str,
                 client_id: int,
                 value: str):
        self.event = event
        self.server_address = f"{client_address[0]}:{client_address[1]}",
        self.client_socket_id = client_socket_id
        self.client_id = client_id
        self.value = value
