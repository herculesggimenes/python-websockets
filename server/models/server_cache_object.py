from dataclasses import dataclass
from datetime import datetime


@dataclass
class ServerCacheObject:
    client_socket_id: str
    client_id: str
    value: str
    created_on: datetime
    update_on: datetime

    def __init__(self, client_socket_id: str, client_id: str, value: str = '0'):
        self.client_id = client_id
        self.client_socket_id = client_socket_id
        self.value = value
        self.created_on = datetime.now()
        self.update_on = datetime.now()

    def update_value(self, value: str):
        self.value = value
        self.update_on = datetime.now()

    def update_client_socket_id(self, client_socket_id: str):
        self.client_socket_id = client_socket_id
        self.update_on = datetime.now()
