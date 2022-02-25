from typing import Tuple

from dataclasses import dataclass
from websocket_server import WebSocketHandler

@dataclass
class ClientWebsocket:
    id:int
    handler:WebSocketHandler
    address: Tuple[str, str]