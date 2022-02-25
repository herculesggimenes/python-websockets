from typing import List, Deque
import os
from server.models.log_event import LogEvent


class Logger:
    def __init__(self):
        # TODO: Substituir cache local por um service de fila, para que outros serviços consumam os dados
        self._cache: list[LogEvent] = list()

    @staticmethod
    def _debug_print_event(event: LogEvent):
        message = f'Event:{event.event},' \
                  f'Server Address:{event.server_address},' \
                  f'Client Id:{event.client_id},' \
                  f'Message:{event.value}'
        print(message)

    def _insert_event_inside_cache(self, event: LogEvent) -> bool:
        success = self._cache.append(event)
        return success

    def register_event(self, event: LogEvent):
        self._insert_event_inside_cache(event)
        self._debug_print_event(event)

    def get_events(self):
        return self._cache
