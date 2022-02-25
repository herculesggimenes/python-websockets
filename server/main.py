import json
import logging
import os
from typing import Dict, Optional, Union

from websocket_server import WebsocketServer
from random import randint

from server.services.logger import Logger
from server.enums.message_type import MessageType
from server.enums.odd_or_even import OddOrEven
from server.models.client_websocket import ClientWebsocket
from server.models.log_event import LogEvent
from server.models.client_message import ClientMessage
from server.models.server_cache_object import ServerCacheObject
from server.models.server_message import ServerMessage


class Server:
    def __init__(self, logger: Logger):
        self._server: WebsocketServer = None
        self._logger = logger
        self._cache: Dict[
            str, ServerCacheObject] = dict()  # TODO: substituir o cache local por um banco REDIS, para garantir a persistência das informações

    @staticmethod
    def _return_odd() -> str:
        initial_number = randint(0, 99)
        is_odd = False if initial_number % 2 else True
        return str(initial_number + 1) if not is_odd else str(initial_number)

    @staticmethod
    def _return_even() -> str:
        initial_number = randint(0, 98)
        is_even = True if initial_number % 2 else False
        return str(initial_number + 1) if not is_even else str(initial_number)

    @staticmethod
    def _return_random() -> str:
        return randint(0, 99)

    @staticmethod
    def _is_json(myjson):
        try:
            json.loads(myjson)
        except ValueError as e:
            return False
        return True

    def _get_client_value_by_client_id(self, client_id: str) -> Union[int, None]:
        if client_id in self._cache:
            return int(self._cache[client_id].value)
        else:
            return None

    def _get_client_id_by_client_websocket_id(self, websocket_id: str) -> Union[str, None]:
        client_id = None
        for cache_object in self._cache.values():
            if websocket_id == cache_object.client_socket_id:
                client_id = cache_object.client_id
                break
        return client_id

    def _create_client(self, client_socket_id: str, client_id: str) -> ServerCacheObject:
        server_cache_object = ServerCacheObject(str(client_socket_id), client_id)
        self._cache[client_id] = server_cache_object
        return server_cache_object

    def _update_client_value(self, client_id: str, value: str):
        self._cache[client_id].update_value(value)

    def _update_client_websocket_id(self, client_id: str, client_socket_id: str = None):

        self._cache[client_id].client_socket_id = client_socket_id

    def _send_error_message_to_client_websocket(self, client_websocket: ClientWebsocket, reason: str):
        server_message = ServerMessage.create_message_json(
            MessageType.ERROR,
            reason
        )
        event = LogEvent(
            server_message.type,
            client_websocket["address"],
            client_websocket["id"],
            self._get_client_id_by_client_websocket_id(client_websocket['id']),
            server_message.value
        )
        self._logger.register_event(event)
        self._server.send_message(
            client_websocket,
            server_message
        )

    def _send_message_to_client_websocket(self, client_websocket: ClientWebsocket, json_payload: str):
        if not self._is_json(json_payload):
            return self._send_error_message_to_client_websocket(client_websocket, 'Not a Json')
        self._server.send_message(
            client_websocket,
            json_payload
        )

    def _set_client_initial_value(self, client_websocket: ClientWebsocket, server: WebsocketServer,
                                  message: ClientMessage):

        client_value = self._get_client_value_by_client_id(message.client_id)

        if not client_value:
            client_value = self._create_client(client_websocket['id'], message.client_id).value

        server_message = ServerMessage.create_message_json(
            MessageType.SET_INITIAL_VALUE,
            client_value
        )

        event = LogEvent(
            message.type,
            client_websocket["address"],
            client_websocket["id"],
            message.client_id,
            server_message
        )
        self._logger.register_event(event)

        server.send_message(
            client_websocket,
            server_message
        )

    def _set_client_incrementer(self, client_websocket: ClientWebsocket, server: WebsocketServer,
                                message: ClientMessage):
        if not OddOrEven.has_value(message.value):
            return self._send_error_message_to_client_websocket(client_websocket, "Invalid OddOrEven")
        incrementer = self._return_even() if message.value == OddOrEven.EVEN.value else self._return_odd()
        server_message = ServerMessage.create_message_json(
            MessageType.INCREMENT,
            incrementer
        )
        event = LogEvent(
            message.type,
            client_websocket["address"],
            client_websocket["id"],
            message.client_id,
            server_message
        )
        self._logger.register_event(event)

        server.send_message(
            client_websocket,
            server_message
        )
        return incrementer

    # Called for every client disconnecting
    def _client_websocket_left(self, client_websocket: ClientWebsocket, server: WebsocketServer) -> None:
        client_id = self._get_client_id_by_client_websocket_id(str(client_websocket['id']))
        if client_id:
            event = LogEvent(MessageType.CONNECTION_CLOSED.value,
                             client_websocket["address"],
                             client_websocket["id"],
                             str(client_id),
                             'disconnected'
                             )
            self._logger.register_event(event)
            self._update_client_websocket_id(client_id)


    # Called for every new client
    def _client_websocket_connected(self, client_websocket: ClientWebsocket, server: WebsocketServer) -> None:
        event = LogEvent(MessageType.CONNECTION_STARTED,
                         client_websocket['address'],
                         client_websocket["id"],
                         'None',
                         'Connected'
                         )
        self._logger.register_event(event)

    # Called when a client sends a message
    def _client_message_received(self, client_websocket: ClientWebsocket, server: WebsocketServer,
                                 raw_message_json: str) -> None:
        message = ClientMessage(raw_message_json)
        event = LogEvent(message.type,
                         client_websocket["address"],
                         client_websocket["id"],
                         message.client_id,
                         message.value
                         )
        self._logger.register_event(event)
        if not MessageType.has_value(message.type):
            return self._send_error_message_to_client_websocket(client_websocket, "Invalid MessageType")
        if message.type == MessageType.HANDSHAKE.value:
            self._set_client_initial_value(client_websocket, server, message)
        elif message.type == MessageType.INCREMENT.value:
            self._set_client_incrementer(client_websocket, server, message)
        elif message.type == MessageType.VALUE.value:
            self._update_client_value(message.client_id, message.value)

    def _start(self) -> None:
        server = WebsocketServer(host=os.getenv("HOST_URL"), port=int(os.getenv("HOST_PORT")))
        server.set_fn_new_client(self._client_websocket_connected)
        server.set_fn_client_left(self._client_websocket_left)
        server.set_fn_message_received(self._client_message_received)
        print("Event:Server Started, Waiting for Client Connection...")
        server.run_forever()

    def start(self) -> None:
        if not self._server:
            self._start()
