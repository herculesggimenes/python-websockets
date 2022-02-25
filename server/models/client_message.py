from dataclasses import dataclass
import json


from server.enums.message_type import MessageType


@dataclass
class ClientMessage:
    client_id:str
    type:MessageType
    value:str

    def __init__(self, raw_message_json: str):
        message_dict = json.loads(raw_message_json)
        self.client_id = message_dict['client_id']
        self.type = message_dict['type']
        self.value = message_dict['value']

    @staticmethod
    def create_message_json(client_id:str, type:MessageType, value:str=''):
        json_dict = {
            'client_id':client_id,
            'type':type.value,
            'value':value,
        }
        return json.dumps(json_dict)