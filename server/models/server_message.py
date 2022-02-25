import json

from dataclasses import dataclass

from server.enums.message_type import MessageType


@dataclass
class ServerMessage:
    type: MessageType
    value: str

    def __init__(self, raw_message_json: str):
        message_dict = json.loads(raw_message_json)
        self.type = message_dict['type']
        self.value = message_dict['value']

    @staticmethod
    def create_message_json(type: MessageType, value: str):
        json_dict = {
            'type': type.value,
            'value': value,
        }
        return json.dumps(json_dict)
