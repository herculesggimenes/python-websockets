import json
import uuid
from random import randint
import _thread
import time
import os
from websocket import WebSocketApp
from client.models.server_message import ServerMessage
from client.models.client_message import ClientMessage
from client.enums.message_type import MessageType
from client.enums.odd_or_even import OddOrEven




class Client:
    def __init__(self):
        self._ws: WebSocketApp = None
        self._value = 0
        self._increment = 1
        self._client_id = str(uuid.uuid4())
        self._handshaken = False

    @staticmethod
    def is_json(myjson):
        try:
            json.loads(myjson)
        except ValueError:
            return False
        return True

    def _send_message_to_server(self, json_payload: str):
        if not self.is_json(json_payload):
            raise ValueError('Invalid Json')
        self._ws.send(
            json_payload
        )

    def _on_server_message(self, ws, raw_message):
        message = ServerMessage(raw_message)
        if not MessageType.has_value(message.type):
            raise ValueError('Invalid MessageType')
        if message.type == MessageType.ERROR.value:
            print(f"###{self._client_id} failed, reason:{message.value} ###")
            raise Exception(message.value)
        elif message.type == MessageType.SET_INITIAL_VALUE.value:  # Initial Value Saved in Server
            print(f"###{self._client_id} setting initial value:{message.value} ###")
            self._value = int(message.value)
            self._handshaken = True
        elif message.type == MessageType.INCREMENT.value:
            print(f"###{self._client_id} incremented from {self._increment} to {message.value} ###")
            self._increment = int(message.value)

    def _on_connection_error(self, ws, error):
        print(f"###{self._client_id} had error {error} ###")

    def _on_connection_close(self, ws, close_status_code, close_msg):
        print(f"###{self._client_id} closed ###")

    def _on_connection_open(self, ws):
        print(f"###{self._client_id} opened ###")
        self._send_message_to_server(
            ClientMessage.create_message_json(
                self._client_id,
                MessageType.HANDSHAKE,
                ''
            )
        )

        def run_update_increment(*args):
            while 1:
                time.sleep(randint(3, 5))
                if self._handshaken:
                    self._send_message_to_server(
                        ClientMessage.create_message_json(
                            self._client_id,
                            MessageType.INCREMENT,
                            OddOrEven.ODD.value if randint(1, 2) == 1 else OddOrEven.EVEN.value
                        )
                    )

        def run_update_value(*args):
            while 1:
                time.sleep(0.5)
                if self._handshaken:
                    self._value += self._increment
                    print(f"###{self._client_id} new value: {self._value} ###")
                    self._send_message_to_server(
                        ClientMessage.create_message_json(
                            self._client_id,
                            MessageType.VALUE,
                            str(self._value)
                        )
                    )

        _thread.start_new_thread(run_update_increment, ())
        _thread.start_new_thread(run_update_value, ())

    def _start(self):
        self._ws = WebSocketApp(os.getenv("SERVER_URL"),
                                on_open=self._on_connection_open,
                                on_message=self._on_server_message,
                                on_error=self._on_connection_error,
                                on_close=self._on_connection_close)
        self._ws.run_forever()

    def start(self):
        if not self._ws:
            self._start()
