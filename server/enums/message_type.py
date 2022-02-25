from enum import Enum


class MessageType(Enum):
    INCREMENT='increment'
    VALUE='value'
    ERROR='error'
    HANDSHAKE='handshake'
    SET_INITIAL_VALUE='set_initial_value'
    CONNECTION_STARTED='connection_started'
    CONNECTION_CLOSED='connection_closed'
    
    @classmethod
    def has_value(self, value):
        return value in self._value2member_map_

